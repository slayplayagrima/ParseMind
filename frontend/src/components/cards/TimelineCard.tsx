import { fallback } from '../../utils/format';

interface TimelineItem {
  label: string;
  value: string | number | null | undefined;
}

interface TimelineCardProps {
  title: string;
  items: TimelineItem[];
}

export const TimelineCard = ({ title, items }: TimelineCardProps) => (
  <section className="bento-card p-8">
    <h2 className="text-lg font-semibold text-brand">{title}</h2>
    <div className="mt-6 space-y-5">
      {items.map((item) => (
        <div key={item.label} className="relative border-l-2 border-dashed border-line pl-5">
          <span className="absolute -left-[7px] top-1 h-3 w-3 rounded-full border-2 border-brand bg-white" />
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-muted">{item.label}</p>
          <p className="mt-1 font-semibold text-ink">{fallback(item.value)}</p>
        </div>
      ))}
    </div>
  </section>
);
