import pytest

from schemas.entities import EntityResponse
from schemas.invoice import InvoiceResponse, LineItem
from schemas.router import RouterResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.errors import DocumentError
from skills import parse_invoice as parse_invoice_module
from skills.validate_invoice import validate_invoice
from workflows import dispatcher, invoice_workflow

ENTITIES = EntityResponse(
    people=[],
    organizations=["Acme Ltd"],
    emails=[],
    phones=[],
    locations=[],
    dates=["2026-11-01"],
    money=["1,180.00"],
    skills=[],
    technologies=[],
)


def make_invoice(**overrides) -> InvoiceResponse:
    """
    A consistent invoice: 2 x 250 + 1 x 500 = 1,000, plus 18% tax = 1,180.
    """

    data = {
        "invoice_number": "INV-042",
        "issue_date": "2026-11-01",
        "due_date": "2026-11-30",
        "currency": "USD",
        "line_items": [
            {"description": "Design", "quantity": 2, "unit_price": 250, "amount": 500},
            {"description": "Hosting", "quantity": 1, "unit_price": 500, "amount": 500},
        ],
        "subtotal": 1000,
        "tax": 180,
        "total": 1180,
    }
    data.update(overrides)
    return InvoiceResponse.model_validate(data)


def skill_response(result):
    return SkillResponse(
        metadata=SkillMetadata(skill="fake", success=True, execution_time_ms=1),
        result=result,
    )


# Schema


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (1250, 1250.0),
        ("1250.5", 1250.5),
        ("$1,250.00", 1250.0),
        ("INR 12,34,567.89", 1234567.89),
        ("-50", -50.0),
        ("n/a", None),
        (None, None),
        (True, None),
    ],
)
def test_amounts_are_parsed_from_model_output(raw, expected):
    assert LineItem(description="x", amount=raw).amount == expected


def test_invoice_fields_default_when_missing():
    invoice = InvoiceResponse.model_validate({})

    assert invoice.line_items == []
    assert invoice.vendor.name is None
    assert invoice.issues == []
    assert invoice.summary == ""


# Validation


def test_consistent_invoice_has_no_issues():
    assert validate_invoice(make_invoice()) == []


def test_rounding_within_a_cent_is_accepted():
    invoice = make_invoice(
        line_items=[{"description": "Widget", "quantity": 3, "unit_price": 33.333, "amount": 100}],
        subtotal=100,
        tax=0,
        total=100,
    )

    assert validate_invoice(invoice) == []


def test_flags_line_item_that_does_not_multiply_out():
    invoice = make_invoice(
        line_items=[
            {"description": "Design", "quantity": 2, "unit_price": 250, "amount": 600},
            {"description": "Hosting", "quantity": 1, "unit_price": 500, "amount": 400},
        ]
    )

    issues = validate_invoice(invoice)

    assert any("Line 'Design'" in issue and "500.00" in issue for issue in issues)
    assert any("Line 'Hosting'" in issue for issue in issues)


def test_flags_subtotal_that_does_not_match_line_items():
    issues = validate_invoice(make_invoice(subtotal=900, total=1080))

    assert issues == ["Line items add up to 1,000.00, but the subtotal is 900.00."]


def test_flags_total_that_does_not_match_subtotal_tax_and_discount():
    issues = validate_invoice(make_invoice(total=1200))

    assert issues == ["Subtotal, tax and discount come to 1,180.00, but the total is 1,200.00."]


def test_discount_is_subtracted_from_total():
    assert validate_invoice(make_invoice(discount=80, total=1100)) == []


def test_flags_due_date_before_issue_date():
    issues = validate_invoice(make_invoice(due_date="2026-10-01"))

    assert issues == ["The due date 2026-10-01 is before the issue date 2026-11-01."]


def test_unparseable_or_missing_dates_are_skipped():
    assert validate_invoice(make_invoice(issue_date="1st Nov", due_date="soon")) == []
    assert validate_invoice(make_invoice(due_date=None)) == []


def test_flags_missing_number_and_total():
    issues = validate_invoice(make_invoice(invoice_number=None, total=None))

    assert "No invoice number was found." in issues
    assert "No total amount was found." in issues


def test_skips_arithmetic_when_values_are_missing():
    invoice = make_invoice(
        line_items=[{"description": "Retainer", "amount": None}],
    )

    assert validate_invoice(invoice) == []


# Skill


def test_parse_invoice_ignores_summary_and_issues_from_model(monkeypatch):
    seen = {}

    def fake_llm(prompt: str):
        seen["prompt"] = prompt
        return {
            "invoice_number": "INV-7",
            "total": "$99.00",
            "summary": "made up",
            "issues": ["made up"],
        }

    monkeypatch.setattr(parse_invoice_module, "generate_json_response", fake_llm)

    response = parse_invoice_module.parse_invoice("Invoice INV-7 total $99")

    assert response.metadata.skill == "parse_invoice"
    assert response.result.total == 99.0
    assert response.result.summary == ""
    assert response.result.issues == []
    assert "Invoice INV-7 total $99" in seen["prompt"]


# Workflow


def test_invoice_workflow_combines_skills_and_checks_totals(monkeypatch):
    monkeypatch.setattr(invoice_workflow, "summarize", lambda _: skill_response("Design invoice."))
    monkeypatch.setattr(
        invoice_workflow, "parse_invoice", lambda _: skill_response(make_invoice(total=1200))
    )
    monkeypatch.setattr(invoice_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    response = invoice_workflow.run("invoice text")
    invoice = response.result.invoice

    assert response.metadata.workflow == "invoice_workflow"
    assert invoice.summary == "Design invoice."
    assert invoice.issues == [
        "Subtotal, tax and discount come to 1,180.00, but the total is 1,200.00."
    ]
    assert response.result.entities == ENTITIES


def test_invoice_workflow_fails_if_a_skill_fails(monkeypatch):
    def broken(_: str):
        raise RuntimeError("LLM request failed")

    monkeypatch.setattr(invoice_workflow, "summarize", lambda _: skill_response(""))
    monkeypatch.setattr(invoice_workflow, "parse_invoice", broken)
    monkeypatch.setattr(invoice_workflow, "extract_entities", lambda _: skill_response(ENTITIES))

    with pytest.raises(RuntimeError, match="LLM request failed"):
        invoice_workflow.run("invoice text")


# Dispatcher


def route(document_type: str, workflow: str | None, supported: bool = True) -> RouterResponse:
    return RouterResponse(
        document_type=document_type, workflow=workflow, supported=supported, confidence=0.9
    )


def test_dispatcher_sends_invoices_to_invoice_workflow(monkeypatch):
    monkeypatch.setitem(dispatcher.WORKFLOWS, "invoice_workflow", lambda text: f"ran on {text}")

    assert dispatcher.dispatch_workflow(route("invoice", "invoice_workflow"), "doc") == "ran on doc"


def test_dispatcher_rejects_types_without_a_workflow():
    with pytest.raises(DocumentError, match="Report documents are not supported yet"):
        dispatcher.dispatch_workflow(route("report", "made_up_workflow"), "doc")


def test_dispatcher_rejects_unsupported_documents():
    with pytest.raises(DocumentError, match="not supported yet"):
        dispatcher.dispatch_workflow(route("unsupported", None, supported=False), "doc")
