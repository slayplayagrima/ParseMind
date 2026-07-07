import { AlertTriangle } from 'lucide-react';

import { Button } from '../buttons/Button';

interface ErrorStateProps {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const ErrorState = ({ title, message, actionLabel, onAction }: ErrorStateProps) => (
  <div className="glass-card mx-auto flex max-w-xl flex-col items-center rounded-[20px] p-10 text-center transition hover:-translate-y-1">
    <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-[#ffdad6]/40 text-critical">
      <AlertTriangle size={30} />
    </div>
    <h2 className="text-lg font-semibold text-brand">{title}</h2>
    <p className="mt-3 max-w-xs text-sm leading-6 text-muted">{message}</p>
    {actionLabel && onAction ? (
      <Button className="mt-6" variant="contained" color="primary" onClick={onAction}>
        {actionLabel}
      </Button>
    ) : null}
  </div>
);
