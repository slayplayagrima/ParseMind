import { fallback } from '../../utils/format';

export interface MetadataItem {
  label: string;
  value: string | number | null | undefined;
}

interface MetadataCardProps {
  title: string;
  items: MetadataItem[];
}

export const MetadataCard = ({ title, items }: MetadataCardProps) => (
  <section className="bento-card p-8">
    <h2 className="text-lg font-semibold text-brand">{title}</h2>
    <dl className="mt-6 space-y-2">
      {items.map((item) => (
        <div key={item.label} className="flex items-center justify-between gap-4 border-b border-line/60 py-3">
          <dt className="text-sm text-muted">{item.label}</dt>
          <dd className="max-w-[55%] break-words text-right text-sm font-bold text-ink">{fallback(item.value)}</dd>
        </div>
      ))}
    </dl>
  </section>
);
