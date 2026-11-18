import threading

import pytest

from schemas.contract import Clause, ContractResponse, Risk
from schemas.entities import EntityResponse
from schemas.resume import Candidate, ResumeResponse
from schemas.skill import SkillMetadata, SkillResponse
from workflows import contract_workflow, resume_workflow


def fresh(result):
    """
    Return a copy of a model so one test can't mutate another's fixture.
    """

    return result.model_copy(deep=True) if hasattr(result, "model_copy") else result


def skill_response(result, name="fake"):
    return SkillResponse(
        metadata=SkillMetadata(skill=name, success=True, execution_time_ms=1),
        result=result,
    )


ENTITIES = EntityResponse(
    people=["Jane Doe"],
    organizations=["Acme"],
    emails=[],
    phones=[],
    locations=[],
    dates=[],
    money=[],
    skills=[],
    technologies=[],
)

CONTRACT = ContractResponse(
    contract_type="Service Agreement",
    title="Acme Services",
    summary="",
    parties=[],
    effective_date=None,
    termination_date=None,
    duration=None,
    governing_law=None,
    jurisdiction=None,
    payment_terms=None,
    obligations=[],
    important_clauses=[],
    risks=[],
    recommendations=[],
)

RISK = Risk(
    title="Unlimited liability",
    severity="high",
    explanation="No cap on damages.",
    recommendation="Add a liability cap.",
)

RESUME = ResumeResponse(
    candidate=Candidate(name="Jane Doe", email="", phone="", location=""),
    summary="",
    education=[],
    experience=[],
    projects=[],
    skills=["Python"],
    certifications=[],
    strengths=[],
    improvements=[],
    ats_score=80,
)


@pytest.fixture
def seen_threads():
    return set()


def recording(result, seen_threads):
    def skill(document_text: str):
        assert document_text == "contract text"
        seen_threads.add(threading.get_ident())
        return skill_response(fresh(result))

    return skill


def test_contract_workflow_combines_all_skills(monkeypatch, seen_threads):
    monkeypatch.setattr(contract_workflow, "summarize", recording("A services deal.", seen_threads))
    monkeypatch.setattr(contract_workflow, "parse_contract", recording(CONTRACT, seen_threads))
    monkeypatch.setattr(contract_workflow, "extract_entities", recording(ENTITIES, seen_threads))
    monkeypatch.setattr(
        contract_workflow,
        "extract_clauses",
        recording([Clause(title="Termination", description="30 days notice")], seen_threads),
    )
    monkeypatch.setattr(contract_workflow, "detect_risks", recording([RISK], seen_threads))

    response = contract_workflow.run("contract text")
    contract = response.result.contract

    assert response.metadata.workflow == "contract_workflow"
    assert contract.summary == "A services deal."
    assert contract.important_clauses[0].title == "Termination"
    assert contract.risks == [RISK]
    assert contract.recommendations == ["Add a liability cap."]
    assert response.result.entities == ENTITIES
    # Skills ran on worker threads, not the caller's thread.
    assert threading.get_ident() not in seen_threads


def test_contract_workflow_fails_if_a_skill_fails(monkeypatch):
    def broken(_: str):
        raise RuntimeError("LLM request failed")

    monkeypatch.setattr(contract_workflow, "summarize", broken)
    for name in ["parse_contract", "extract_entities", "extract_clauses", "detect_risks"]:
        monkeypatch.setattr(contract_workflow, name, lambda _: skill_response([]))

    with pytest.raises(RuntimeError, match="LLM request failed"):
        contract_workflow.run("contract text")


def test_resume_workflow_combines_all_skills(monkeypatch, seen_threads):
    def text(result):
        def skill(document_text: str):
            seen_threads.add(threading.get_ident())
            return skill_response(fresh(result))

        return skill

    monkeypatch.setattr(resume_workflow, "summarize", text("Backend engineer."))
    monkeypatch.setattr(resume_workflow, "parse_resume", text(RESUME))
    monkeypatch.setattr(resume_workflow, "extract_entities", text(ENTITIES))

    response = resume_workflow.run("resume text")

    assert response.metadata.workflow == "resume_workflow"
    assert response.result.resume.summary == "Backend engineer."
    assert response.result.resume.skills == ["Python"]
    assert response.result.entities == ENTITIES
    assert threading.get_ident() not in seen_threads
