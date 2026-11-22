import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import type { ReportWorkflowResult, WorkflowResponse } from '../../../types/workflow';
import { WorkflowRenderer } from '../shared/WorkflowRenderer';
import { ReportRenderer } from './ReportRenderer';

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

const result: ReportWorkflowResult = {
  report: {
    title: 'Annual Report 2026',
    report_type: 'Annual report',
    authors: ['Dr. Rao', 'J. Lee'],
    organization: 'Acme Research',
    publication_date: '2026-03-01',
    purpose: 'Review the year.',
    key_findings: ['Revenue grew 12%.', 'Churn fell to 3%.'],
    metrics: [{ name: 'Revenue', value: '$4.2M', context: 'FY2026' }],
    conclusions: ['The strategy is working.'],
    recommendations: ['Expand to two new markets.'],
    limitations: [],
    summary: 'A strong year for Acme.',
  },
  entities,
};

describe('ReportRenderer', () => {
  it('shows the summary, findings, figures and recommendations', () => {
    render(<ReportRenderer result={result} />);

    expect(screen.getByText('A strong year for Acme.')).toBeInTheDocument();
    expect(screen.getByText('Revenue grew 12%.')).toBeInTheDocument();
    expect(screen.getByText('$4.2M')).toBeInTheDocument();
    expect(screen.getByText('Expand to two new markets.')).toBeInTheDocument();
    expect(screen.getByText('Dr. Rao, J. Lee')).toBeInTheDocument();
  });

  it('is picked by the workflow renderer for report results', () => {
    const response: WorkflowResponse = {
      metadata: {
        workflow: 'report_workflow',
        success: true,
        model: 'openai/gpt-oss-120b',
        confidence: 0.95,
        execution_time_ms: 900,
      },
      result,
    };

    render(<WorkflowRenderer response={response} />);

    expect(screen.getByText('Key Figures')).toBeInTheDocument();
    expect(screen.queryByText(/renderer unavailable/)).not.toBeInTheDocument();
  });
});
