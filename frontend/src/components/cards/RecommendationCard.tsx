import { CheckCircle2 } from 'lucide-react';

interface RecommendationCardProps {
  title: string;
  recommendations: string[];
}

export const RecommendationCard = ({ title, recommendations }: RecommendationCardProps) => (
  <section className="bento-card p-8">
      <h2 className="text-lg font-semibold text-brand">{title}</h2>
      <div className="mt-6 space-y-3">
        {recommendations.length > 0 ? (
          recommendations.map((recommendation) => (
            <div key={recommendation} className="flex gap-3 rounded-xl border border-line/60 bg-surface-low p-4">
              <CheckCircle2 className="mt-0.5 shrink-0 text-brand" size={18} />
              <p className="text-sm text-ink">{recommendation}</p>
            </div>
          ))
        ) : (
          <p className="text-sm text-muted">-</p>
        )}
      </div>
  </section>
);
