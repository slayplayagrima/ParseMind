import { Chip } from '@mui/material';

type StatusTone = 'neutral' | 'success' | 'warning' | 'danger' | 'info';

interface StatusBadgeProps {
  label: string;
  tone?: StatusTone;
}

const toneStyles: Record<StatusTone, { bg: string; color: string }> = {
  neutral: { bg: '#e9e8e6', color: '#44474d' },
  success: { bg: '#f4f3f1', color: '#166534' },
  warning: { bg: '#fddfa8', color: '#58441b' },
  danger: { bg: '#ffdad6', color: '#632024' },
  info: { bg: '#f4f3f1', color: '#25344f' },
};

export const StatusBadge = ({ label, tone = 'neutral' }: StatusBadgeProps) => {
  const styles = toneStyles[tone];

  return (
    <Chip
      label={label}
      size="small"
      sx={{
        backgroundColor: styles.bg,
        color: styles.color,
        borderRadius: '8px',
        height: 24,
        fontSize: 10,
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
      }}
    />
  );
};
