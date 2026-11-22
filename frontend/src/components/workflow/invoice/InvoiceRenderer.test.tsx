import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import type { InvoiceWorkflowResult, WorkflowResponse } from '../../../types/workflow';
import { WorkflowRenderer } from '../shared/WorkflowRenderer';
import { InvoiceRenderer } from './InvoiceRenderer';

const entities = {
  people: [],
  organizations: ['Acme Ltd'],
  emails: [],
  phones: [],
  locations: [],
  dates: [],
  money: [],
  skills: [],
  technologies: [],
};

const makeResult = (issues: string[] = []): InvoiceWorkflowResult => ({
  invoice: {
    invoice_number: 'INV-042',
    issue_date: '2026-11-01',
    due_date: '2026-11-30',
    currency: 'USD',
    vendor: { name: 'Acme Ltd', address: null, email: 'billing@acme.test', tax_id: null },
    customer: { name: 'Beta Inc', address: null, email: null, tax_id: null },
    line_items: [{ description: 'Design work', quantity: 2, unit_price: 250, amount: 500 }],
    subtotal: 500,
    tax: 90,
    discount: null,
    total: 590,
    payment_terms: 'Net 30',
    summary: 'Design invoice from Acme to Beta.',
    issues,
  },
  entities,
});

describe('InvoiceRenderer', () => {
  it('shows the invoice details, line items and totals', () => {
    render(<InvoiceRenderer result={makeResult()} />);

    expect(screen.getByText('INV-042')).toBeInTheDocument();
    expect(screen.getByText('Design invoice from Acme to Beta.')).toBeInTheDocument();
    expect(screen.getByText('Design work')).toBeInTheDocument();
    expect(screen.getByText('Beta Inc')).toBeInTheDocument();
    expect(screen.getAllByText('$590.00').length).toBeGreaterThan(0);
    expect(screen.getAllByText('$250.00').length).toBeGreaterThan(0);
  });

  it('says the invoice checks out when there are no issues', () => {
    render(<InvoiceRenderer result={makeResult()} />);

    const checks = screen.getByRole('region', { name: 'Invoice checks' });
    expect(within(checks).getByText(/All totals add up/)).toBeInTheDocument();
  });

  it('lists every issue the backend found', () => {
    const issues = [
      'Subtotal, tax and discount come to 590.00, but the total is 600.00.',
      'The due date 2026-10-01 is before the issue date 2026-11-01.',
    ];

    render(<InvoiceRenderer result={makeResult(issues)} />);

    const checks = screen.getByRole('region', { name: 'Invoice checks' });
    for (const issue of issues) {
      expect(within(checks).getByText(issue)).toBeInTheDocument();
    }
    expect(within(checks).queryByText(/All totals add up/)).not.toBeInTheDocument();
  });

  it('is picked by the workflow renderer for invoice results', () => {
    const response: WorkflowResponse = {
      metadata: {
        workflow: 'invoice_workflow',
        success: true,
        model: 'openai/gpt-oss-120b',
        confidence: 0.95,
        execution_time_ms: 1200,
      },
      result: makeResult(),
    };

    render(<WorkflowRenderer response={response} />);

    expect(screen.getByText('Line Items')).toBeInTheDocument();
    expect(screen.queryByText(/renderer unavailable/)).not.toBeInTheDocument();
  });
});
