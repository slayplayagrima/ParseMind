import { FileText } from 'lucide-react';

interface BrandMarkProps {
  compact?: boolean;
}

export const BrandMark = ({ compact = false }: BrandMarkProps) => (
  <span className="inline-flex items-center gap-3">
    <span className="flex h-7 w-7 items-center justify-center text-brand">
      <FileText size={compact ? 18 : 22} strokeWidth={2} />
    </span>
    <span className={compact ? 'text-lg font-bold text-brand' : 'text-[22px] font-bold text-brand'}>
      ParseMind
    </span>
  </span>
);
