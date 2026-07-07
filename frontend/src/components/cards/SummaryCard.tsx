import { fallback } from '../../utils/format';

interface SummaryCardProps {
  title: string;
  value: string | number | null | undefined;
  description?: string;
}

export const SummaryCard = ({ title, value, description }: SummaryCardProps) => (
  <article className="bento-card p-5">
    <p className="text-xs font-bold uppercase tracking-[0.14em] text-muted">{title}</p>
    <p className="mt-3 break-words text-3xl font-bold tracking-tight text-brand">{fallback(value)}</p>
    {description ? <p className="mt-2 text-sm text-muted">{description}</p> : null}
  </article>
);
