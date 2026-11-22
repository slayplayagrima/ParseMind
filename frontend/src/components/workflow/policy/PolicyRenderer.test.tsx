import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import type { ContractRisk, PolicyWorkflowResult, WorkflowResponse } from '../../../types/workflow';
import { WorkflowRenderer } from '../shared/WorkflowRenderer';
import { PolicyRenderer } from './PolicyRenderer';

const entities = {
  people: [],
  organizations: [],
  emails: [],
  phones: [],
  locations: [],
  dates: [],
  money: [],
  skills: [],
  technologies: [],
};

const makeResult = (gaps: ContractRisk[]): PolicyWorkflowResult => ({
  policy: {
    title: 'Privacy Policy',
    policy_type: 'Privacy policy',
    organization: 'Acme Inc',
    effective_date: '2026-01-01',
    version: '2.1',
    scope: 'All customer data.',
    applies_to: ['All users', 'Contractors'],
    rules: [{ title: 'Consent', description: 'We ask before collecting data.' }],
    obligations: ['Report breaches within 72 hours.'],
    prohibited: ['Selling personal data.'],
    penalties: [],
    compliance_gaps: gaps,
    summary: 'How Acme handles personal data.',
  },
  entities,
});

const gaps: ContractRisk[] = [
  {
    title: 'No retention period',
    severity: 'high',
    explanation: 'The policy never says how long data is kept.',
    recommendation: 'State a retention period for each data type.',
  },
  {
    title: 'No review date',
    severity: 'low',
    explanation: 'There is no scheduled review.',
    recommendation: 'Review the policy every year.',
  },
];

describe('PolicyRenderer', () => {
  it('shows the rules, obligations and who the policy applies to', () => {
    render(<PolicyRenderer result={makeResult(gaps)} />);

    expect(screen.getByText('How Acme handles personal data.')).toBeInTheDocument();
    expect(screen.getByText('Consent')).toBeInTheDocument();
    expect(screen.getByText('Report breaches within 72 hours.')).toBeInTheDocument();
    expect(screen.getByText('Selling personal data.')).toBeInTheDocument();
    expect(screen.getByText('Contractors')).toBeInTheDocument();
  });

  it('lists compliance gaps and counts the serious ones', () => {
    render(<PolicyRenderer result={makeResult(gaps)} />);

    expect(screen.getByText('No retention period')).toBeInTheDocument();
    expect(screen.getByText('State a retention period for each data type.')).toBeInTheDocument();
    expect(screen.getByText('1 high or critical')).toBeInTheDocument();
  });

  it('says so when no gaps were found', () => {
    render(<PolicyRenderer result={makeResult([])} />);

    expect(screen.getByText('No compliance gaps were found.')).toBeInTheDocument();
  });

  it('is picked by the workflow renderer for policy results', () => {
    const response: WorkflowResponse = {
      metadata: {
        workflow: 'policy_workflow',
        success: true,
        model: 'openai/gpt-oss-120b',
        confidence: 0.95,
        execution_time_ms: 900,
      },
      result: makeResult(gaps),
    };

    render(<WorkflowRenderer response={response} />);

    expect(screen.getByRole('heading', { name: 'Rules' })).toBeInTheDocument();
    expect(screen.queryByText(/renderer unavailable/)).not.toBeInTheDocument();
  });
});
