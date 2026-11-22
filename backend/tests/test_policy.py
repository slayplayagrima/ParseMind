import pytest

from schemas.entities import EntityResponse
from schemas.policy import ComplianceGap, PolicyResponse
from schemas.router import RouterResponse
from schemas.skill import SkillMetadata, SkillResponse
from skills import parse_policy as parse_policy_module
from workflows import dispatcher, policy_workflow

ENTITIES = EntityResponse(
    people=[],
    organizations=["Acme Inc"],
    emails=["privacy@acme.test"],
    phones=[],
    locations=[],
    dates=["2026-01-01"],
    money=[],
    skills=[],
    technologies=[],
)


def skill_response(result):
    return SkillResponse(
        metadata=SkillMetadata(skill="fake", success=True, execution_time_ms=1),
        result=result,
    )


def gap(severity) -> ComplianceGap:
    return ComplianceGap(
        title="No retention period",
        severity=severity,
        explanation="The policy never says how long data is kept.",
        recommendation="State a retention period for each data type.",
    )


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("high", "high"),
        ("High", "high"),
        (" CRITICAL ", "critical"),
        ("moderate", "medium"),
        ("severe", "high"),
        ("minor", "low"),
        ("unknown", "medium"),
        (None, "medium"),
    ],
)
def test_gap_severity_is_normalized(raw, expected):
    assert gap(raw).severity == expected


def test_policy_fields_default_when_missing():
    policy = PolicyResponse.model_validate({})

    assert policy.rules == []
    assert policy.compliance_gaps == []
    assert policy.summary == ""


def test_parse_policy_reads_rules_and_gaps(monkeypatch):
    seen = {}

    def fake_llm(prompt: str):
        seen["prompt"] = prompt
        return {
            "title": "Privacy Policy",
            "policy_type": "Privacy policy",
            "applies_to": ["All users"],
            "rules": [{"title": "Consent", "description": "We ask before collecting data."}],
            "prohibited": ["Selling personal data"],
            "compliance_gaps": [
                {
                    "title": "No retention period",
                    "severity": "High",
                    "explanation": "Missing.",
                    "recommendation": "Add one.",
                }
            ],
            "summary": "made up by the model",
        }

    monkeypatch.setattr(parse_policy_module, "generate_json_response", fake_llm)

    response = parse_policy_module.parse_policy("Acme privacy policy text")
    policy = response.result

    assert response.metadata.skill == "parse_policy"
    assert policy.rules[0].title == "Consent"
    assert policy.compliance_gaps[0].severity == "high"
    assert policy.summary == ""
    assert "Acme privacy policy text" in seen["prompt"]


def test_policy_workflow_combines_skills(monkeypatch):
    policy = PolicyResponse(title="Code of Conduct", compliance_gaps=[gap("low")])

    monkeypatch.setattr(policy_workflow, "summarize", lambda _: skill_response("Staff rules."))
    monkeypatch.setattr(policy_workflow, "parse_policy", lambda _: skill_response(policy))
    monkeypatch.setattr(policy_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    response = policy_workflow.run("policy text")

    assert response.metadata.workflow == "policy_workflow"
    assert response.result.policy.summary == "Staff rules."
    assert response.result.policy.compliance_gaps[0].severity == "low"
    assert response.result.entities == ENTITIES


def test_policy_workflow_fails_if_a_skill_fails(monkeypatch):
    def broken(_: str):
        raise RuntimeError("LLM request failed")

    monkeypatch.setattr(policy_workflow, "summarize", lambda _: skill_response(""))
    monkeypatch.setattr(policy_workflow, "parse_policy", broken)
    monkeypatch.setattr(policy_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    with pytest.raises(RuntimeError, match="LLM request failed"):
        policy_workflow.run("policy text")


def test_dispatcher_sends_policies_to_policy_workflow(monkeypatch):
    monkeypatch.setitem(dispatcher.WORKFLOWS, "policy_workflow", lambda text: f"policy: {text}")
    route = RouterResponse(
        document_type="policy", workflow="policy_workflow", supported=True, confidence=0.9
    )

    assert dispatcher.dispatch_workflow(route, "doc") == "policy: doc"
