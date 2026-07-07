import { BarChart3, FileSearch } from 'lucide-react';

import { Button } from '../buttons/Button';

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState = ({ title, description, actionLabel, onAction }: EmptyStateProps) => (
  <div className="glass-card mx-auto flex max-w-xl flex-col items-center rounded-[20px] border-dashed p-10 text-center transition hover:-translate-y-1">
    <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-surface-low text-brand">
      {title.toLowerCase().includes('data') ? <BarChart3 size={30} /> : <FileSearch size={30} />}
    </div>
    <h2 className="text-lg font-semibold text-brand">{title}</h2>
    <p className="mt-3 max-w-xs text-sm leading-6 text-muted">{description}</p>
    {actionLabel && onAction ? (
      <Button className="mt-6" variant="contained" onClick={onAction}>
        {actionLabel}
      </Button>
    ) : null}
  </div>
);
