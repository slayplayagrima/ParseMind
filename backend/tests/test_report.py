import pytest

from schemas.entities import EntityResponse
from schemas.report import ReportResponse
from schemas.router import RouterResponse
from schemas.skill import SkillMetadata, SkillResponse
from skills import parse_report as parse_report_module
from workflows import dispatcher, report_workflow

ENTITIES = EntityResponse(
    people=["Dr. Rao"],
    organizations=["Acme Research"],
    emails=[],
    phones=[],
    locations=[],
    dates=["2026"],
    money=["$4.2M"],
    skills=[],
    technologies=[],
)


def skill_response(result):
    return SkillResponse(
        metadata=SkillMetadata(skill="fake", success=True, execution_time_ms=1),
        result=result,
    )


def test_report_fields_default_when_missing():
    report = ReportResponse.model_validate({})

    assert report.key_findings == []
    assert report.metrics == []
    assert report.title is None
    assert report.summary == ""


def test_parse_report_reads_findings_and_metrics(monkeypatch):
    seen = {}

    def fake_llm(prompt: str):
        seen["prompt"] = prompt
        return {
            "title": "Annual Report 2026",
            "report_type": "Annual report",
            "authors": ["Dr. Rao"],
            "key_findings": ["Revenue grew 12%."],
            "metrics": [{"name": "Revenue", "value": "$4.2M", "context": "FY2026"}],
            "recommendations": ["Expand to two new markets."],
            "summary": "made up by the model",
        }

    monkeypatch.setattr(parse_report_module, "generate_json_response", fake_llm)

    response = parse_report_module.parse_report("Acme annual report text")
    report = response.result

    assert response.metadata.skill == "parse_report"
    assert report.title == "Annual Report 2026"
    assert report.metrics[0].value == "$4.2M"
    assert report.key_findings == ["Revenue grew 12%."]
    # The summary comes from its own skill.
    assert report.summary == ""
    assert "Acme annual report text" in seen["prompt"]


def test_report_workflow_combines_skills(monkeypatch):
    report = ReportResponse(title="Market Analysis", key_findings=["Demand is rising."])

    monkeypatch.setattr(report_workflow, "summarize", lambda _: skill_response("A market study."))
    monkeypatch.setattr(report_workflow, "parse_report", lambda _: skill_response(report))
    monkeypatch.setattr(report_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    response = report_workflow.run("report text")

    assert response.metadata.workflow == "report_workflow"
    assert response.result.report.summary == "A market study."
    assert response.result.report.key_findings == ["Demand is rising."]
    assert response.result.entities == ENTITIES


def test_report_workflow_fails_if_a_skill_fails(monkeypatch):
    def broken(_: str):
        raise RuntimeError("LLM request failed")

    monkeypatch.setattr(report_workflow, "summarize", lambda _: skill_response(""))
    monkeypatch.setattr(report_workflow, "parse_report", broken)
    monkeypatch.setattr(report_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    with pytest.raises(RuntimeError, match="LLM request failed"):
        report_workflow.run("report text")


def test_dispatcher_sends_reports_to_report_workflow(monkeypatch):
    monkeypatch.setitem(dispatcher.WORKFLOWS, "report_workflow", lambda text: f"report: {text}")
    route = RouterResponse(
        document_type="report", workflow="report_workflow", supported=True, confidence=0.9
    )

    assert dispatcher.dispatch_workflow(route, "doc") == "report: doc"
