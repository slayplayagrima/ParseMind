import type { ContractRisk, RiskSeverity } from '../../types/workflow';
import { titleCase } from '../../utils/format';
import { StatusBadge } from '../common/StatusBadge';

interface RiskCardProps {
  risks: ContractRisk[];
}

const severityTone: Record<RiskSeverity, 'success' | 'warning' | 'danger'> = {
  low: 'success',
  medium: 'warning',
  high: 'danger',
  critical: 'danger',
};

export const RiskCard = ({ risks }: RiskCardProps) => (
  <section className="bento-card p-8">
      <h2 className="text-lg font-semibold text-brand">Risk Assessment</h2>
      <div className="mt-6 space-y-4">
        {risks.length > 0 ? (
          risks.map((risk) => (
            <article key={`${risk.title}-${risk.severity}`} className="rounded-xl border border-line/60 bg-surface-low p-4">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <h3 className="font-bold text-brand">{risk.title}</h3>
                <StatusBadge label={titleCase(risk.severity)} tone={severityTone[risk.severity]} />
              </div>
              <p className="mt-3 text-sm text-muted">{risk.explanation}</p>
              <p className="mt-3 text-sm font-semibold text-ink">{risk.recommendation}</p>
            </article>
          ))
        ) : (
          <p className="text-sm text-muted">-</p>
        )}
      </div>
  </section>
);
