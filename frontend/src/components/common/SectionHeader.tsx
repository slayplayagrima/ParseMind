import { Typography } from '@mui/material';

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
}

export const SectionHeader = ({ eyebrow, title, description }: SectionHeaderProps) => (
  <div className="space-y-2">
    {eyebrow ? (
      <Typography className="font-bold uppercase tracking-[0.22em] text-coffee" variant="caption">
        {eyebrow}
      </Typography>
    ) : null}
    <Typography variant="h4" className="text-brand">
      {title}
    </Typography>
    {description ? (
      <Typography variant="body1" className="max-w-3xl text-secondary">
        {description}
      </Typography>
    ) : null}
  </div>
);
