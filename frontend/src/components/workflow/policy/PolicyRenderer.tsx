import { Chip } from '@mui/material';
import { Sparkles } from 'lucide-react';

import { EntityCard } from '../../cards/EntityCard';
import { MetadataCard } from '../../cards/MetadataCard';
import { RecommendationCard } from '../../cards/RecommendationCard';
import { RiskCard } from '../../cards/RiskCard';
import { SummaryCard } from '../../cards/SummaryCard';
import { Accordion } from '../../common/Accordion';
import type { PolicyWorkflowResult } from '../../../types/workflow';
import { fallback } from '../../../utils/format';

interface PolicyRendererProps {
  result: PolicyWorkflowResult;
}

export const PolicyRenderer = ({ result }: PolicyRendererProps) => {
  const { policy, entities } = result;
  const seriousGaps = policy.compliance_gaps.filter(
    (gap) => gap.severity === 'high' || gap.severity === 'critical',
  ).length;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
      <div className="md:col-span-3">
        <SummaryCard title="Policy Type" value={policy.policy_type} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Rules" value={policy.rules.length} description="Main provisions" />
      </div>
      <div className="md:col-span-3">
        <SummaryCard
          title="Compliance Gaps"
          value={policy.compliance_gaps.length}
          description={`${seriousGaps} high or critical`}
        />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Effective" value={policy.effective_date} />
      </div>

      <section className="bento-card p-8 md:col-span-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-brand">
            <Sparkles size={18} />
            Policy Summary
          </h2>
          <span className="rounded-full bg-[#fddfa8] px-3 py-1 text-xs font-bold text-[#261900]">AI SYNTHESIS</span>
        </div>
        <p className="text-base leading-7 text-muted">{fallback(policy.summary)}</p>
        <div className="mt-6 flex flex-wrap gap-2">
          {policy.applies_to.map((group) => (
            <Chip key={group} label={group} />
          ))}
        </div>
      </section>

      <div className="md:col-span-4">
        <MetadataCard
          title="Details"
          items={[
            { label: 'Title', value: policy.title },
            { label: 'Organization', value: policy.organization },
            { label: 'Version', value: policy.version },
            { label: 'Scope', value: policy.scope },
          ]}
        />
      </div>

      <section className="bento-card p-8 md:col-span-7">
        <h2 className="mb-5 text-lg font-semibold text-brand">Rules</h2>
        <Accordion
          items={
            policy.rules.length > 0
              ? policy.rules.map((rule) => ({
                  title: rule.title,
                  content: <p className="text-sm text-muted">{fallback(rule.description)}</p>,
                }))
              : [{ title: '-', content: <p className="text-sm text-muted">-</p> }]
          }
        />
      </section>

      <div className="md:col-span-5">
        <RiskCard
          title="Compliance Gaps"
          risks={policy.compliance_gaps}
          emptyLabel="No compliance gaps were found."
        />
      </div>

      <div className="md:col-span-4">
        <RecommendationCard title="Obligations" recommendations={policy.obligations} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Prohibited" recommendations={policy.prohibited} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Penalties" recommendations={policy.penalties} />
      </div>

      <div className="md:col-span-12">
        <EntityCard entities={entities} />
      </div>
    </div>
  );
};
