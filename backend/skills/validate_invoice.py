from datetime import date

from schemas.invoice import InvoiceResponse

# Allow for rounding on each line and on the totals.
TOLERANCE = 0.01


def _differs(a: float, b: float) -> bool:
    return abs(a - b) > TOLERANCE


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _money(value: float) -> str:
    return f"{value:,.2f}"


def validate_invoice(invoice: InvoiceResponse) -> list[str]:
    """
    Check an extracted invoice for arithmetic and consistency problems.

    Runs locally without the LLM, so the checks are exact and repeatable.
    """

    issues: list[str] = []

    for item in invoice.line_items:
        if None not in (item.quantity, item.unit_price, item.amount):
            expected = item.quantity * item.unit_price
            if _differs(expected, item.amount):
                issues.append(
                    f"Line '{item.description}': {item.quantity:g} x "
                    f"{_money(item.unit_price)} = {_money(expected)}, "
                    f"but the invoice shows {_money(item.amount)}."
                )

    amounts = [item.amount for item in invoice.line_items]

    if invoice.subtotal is not None and amounts and None not in amounts:
        line_total = sum(amounts)
        if _differs(line_total, invoice.subtotal):
            issues.append(
                f"Line items add up to {_money(line_total)}, "
                f"but the subtotal is {_money(invoice.subtotal)}."
            )

    if invoice.subtotal is not None and invoice.total is not None:
        expected_total = invoice.subtotal + (invoice.tax or 0) - (invoice.discount or 0)
        if _differs(expected_total, invoice.total):
            issues.append(
                f"Subtotal, tax and discount come to {_money(expected_total)}, "
                f"but the total is {_money(invoice.total)}."
            )

    issued = _parse_date(invoice.issue_date)
    due = _parse_date(invoice.due_date)

    if issued and due and due < issued:
        issues.append(f"The due date {due} is before the issue date {issued}.")

    if not invoice.invoice_number:
        issues.append("No invoice number was found.")

    if invoice.total is None:
        issues.append("No total amount was found.")

    return issues
