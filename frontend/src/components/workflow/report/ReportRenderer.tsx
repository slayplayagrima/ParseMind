import { Sparkles } from 'lucide-react';

import { EntityCard } from '../../cards/EntityCard';
import { MetadataCard } from '../../cards/MetadataCard';
import { RecommendationCard } from '../../cards/RecommendationCard';
import { SummaryCard } from '../../cards/SummaryCard';
import { Table } from '../../tables/Table';
import type { ReportWorkflowResult } from '../../../types/workflow';
import { fallback } from '../../../utils/format';

interface ReportRendererProps {
  result: ReportWorkflowResult;
}

export const ReportRenderer = ({ result }: ReportRendererProps) => {
  const { report, entities } = result;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
      <div className="md:col-span-4">
        <SummaryCard title="Report Type" value={report.report_type} />
      </div>
      <div className="md:col-span-4">
        <SummaryCard title="Key Findings" value={report.key_findings.length} description="Main results" />
      </div>
      <div className="md:col-span-4">
        <SummaryCard title="Published" value={report.publication_date} />
      </div>

      <section className="bento-card p-8 md:col-span-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-brand">
            <Sparkles size={18} />
            Report Summary
          </h2>
          <span className="rounded-full bg-[#fddfa8] px-3 py-1 text-xs font-bold text-[#261900]">AI SYNTHESIS</span>
        </div>
        <p className="text-base leading-7 text-muted">{fallback(report.summary)}</p>
      </section>

      <div className="md:col-span-4">
        <MetadataCard
          title="Details"
          items={[
            { label: 'Title', value: report.title },
            { label: 'Organization', value: report.organization },
            { label: 'Authors', value: report.authors.join(', ') },
            { label: 'Purpose', value: report.purpose },
          ]}
        />
      </div>

      <div className="md:col-span-6">
        <RecommendationCard title="Key Findings" recommendations={report.key_findings} />
      </div>
      <section className="bento-card p-8 md:col-span-6">
        <h2 className="mb-5 text-lg font-semibold text-brand">Key Figures</h2>
        <Table
          columns={[
            { key: 'name', label: 'Metric' },
            { key: 'value', label: 'Value' },
            { key: 'context', label: 'Context' },
          ]}
          rows={report.metrics}
        />
      </section>

      <div className="md:col-span-4">
        <RecommendationCard title="Conclusions" recommendations={report.conclusions} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Recommendations" recommendations={report.recommendations} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Limitations" recommendations={report.limitations} />
      </div>

      <div className="md:col-span-12">
        <EntityCard entities={entities} />
      </div>
    </div>
  );
};
