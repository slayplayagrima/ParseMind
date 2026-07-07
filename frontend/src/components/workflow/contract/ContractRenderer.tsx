import { Sparkles } from 'lucide-react';

import { EntityCard } from '../../cards/EntityCard';
import { MetadataCard } from '../../cards/MetadataCard';
import { RecommendationCard } from '../../cards/RecommendationCard';
import { RiskCard } from '../../cards/RiskCard';
import { SummaryCard } from '../../cards/SummaryCard';
import { TimelineCard } from '../../cards/TimelineCard';
import { Accordion } from '../../common/Accordion';
import { Table } from '../../tables/Table';
import type { ContractWorkflowResult } from '../../../types/workflow';
import { fallback } from '../../../utils/format';

interface ContractRendererProps {
  result: ContractWorkflowResult;
}

export const ContractRenderer = ({ result }: ContractRendererProps) => {
  const { contract, entities } = result;
  const paymentTerms = contract.payment_terms;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
      <div className="md:col-span-3">
        <SummaryCard title="Parties" value={contract.parties.length} description="Identified entities" />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Key Clauses" value={contract.important_clauses.length} description="Extracted provisions" />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Risk Alerts" value={contract.risks.length} description="Review recommended" />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Obligations" value={contract.obligations.length} description={contract.duration ?? 'Contract duties'} />
      </div>

      <section className="bento-card p-8 md:col-span-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-brand">
            <Sparkles size={18} />
            Executive Summary
          </h2>
          <span className="rounded-full bg-[#fddfa8] px-3 py-1 text-xs font-bold text-[#261900]">AI SYNTHESIS</span>
        </div>
        <p className="text-base leading-7 text-muted">{fallback(contract.summary)}</p>
        <div className="mt-5 rounded-xl border-l-4 border-brand bg-surface-low p-5 text-sm italic leading-6 text-ink">
          {fallback(contract.recommendations[0] ?? contract.risks[0]?.recommendation)}
        </div>
      </section>

      <div className="md:col-span-4">
        <MetadataCard
          title="Document Metadata"
          items={[
            { label: 'Contract Type', value: contract.contract_type },
            { label: 'Title', value: contract.title },
            { label: 'Duration', value: contract.duration },
            { label: 'Jurisdiction', value: contract.jurisdiction },
            { label: 'Governing Law', value: contract.governing_law },
          ]}
        />
      </div>

      <section className="bento-card p-8 md:col-span-12">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-brand">Workflow: Contract Insight</h2>
            <p className="mt-1 text-sm text-muted">Analyzing legal provisions and operational timelines.</p>
          </div>
        </div>
        <Accordion
          items={[
            {
              title: 'Important Clauses',
              content:
                contract.important_clauses.length > 0 ? (
                  <div className="space-y-4">
                    {contract.important_clauses.map((clause) => (
                      <div key={clause.title}>
                        <p className="font-semibold text-brand">{clause.title}</p>
                        <p className="mt-1 text-sm leading-6 text-muted">{clause.description}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted">—</p>
                ),
            },
            {
              title: 'Payment Terms & Obligations',
              content: (
                <div className="space-y-4">
                  <dl className="grid gap-3 md:grid-cols-4">
                    <div>
                      <dt className="text-xs uppercase text-muted">Amount</dt>
                      <dd className="font-semibold">{fallback(paymentTerms?.amount)}</dd>
                    </div>
                    <div>
                      <dt className="text-xs uppercase text-muted">Currency</dt>
                      <dd className="font-semibold">{fallback(paymentTerms?.currency)}</dd>
                    </div>
                    <div>
                      <dt className="text-xs uppercase text-muted">Due Date</dt>
                      <dd className="font-semibold">{fallback(paymentTerms?.due_date)}</dd>
                    </div>
                    <div>
                      <dt className="text-xs uppercase text-muted">Frequency</dt>
                      <dd className="font-semibold">{fallback(paymentTerms?.frequency)}</dd>
                    </div>
                  </dl>
                  <RecommendationCard title="Obligations" recommendations={contract.obligations} />
                </div>
              ),
            },
            {
              title: 'Execution Timeline',
              content: (
                <TimelineCard
                  title="Important Dates"
                  items={[
                    { label: 'Effective Date', value: contract.effective_date },
                    { label: 'Termination Date', value: contract.termination_date },
                  ]}
                />
              ),
            },
          ]}
        />
      </section>

      <section className="bento-card p-8 md:col-span-5">
        <h2 className="mb-5 text-lg font-semibold text-brand">Parties</h2>
            <Table
              columns={[
                { key: 'name', label: 'Name' },
                { key: 'role', label: 'Role' },
              ]}
              rows={contract.parties}
            />
      </section>

      <div className="md:col-span-7">
        <RiskCard risks={contract.risks} />
      </div>
      <div className="md:col-span-8">
        <EntityCard entities={entities} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Action Items" recommendations={contract.recommendations} />
      </div>
    </div>
  );
};
