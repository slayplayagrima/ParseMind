export const fallback = (value: string | number | null | undefined): string => {
  if (value === null || value === undefined || value === '') {
    return '—';
  }

  return String(value);
};

export const titleCase = (value: string): string =>
  value
    .replace(/[_-]/g, ' ')
    .replace(/\w\S*/g, (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase());

export const formatMilliseconds = (milliseconds: number | null | undefined): string => {
  if (milliseconds === null || milliseconds === undefined) {
    return '-';
  }

  if (milliseconds < 1000) {
    return `${milliseconds} ms`;
  }

  return `${(milliseconds / 1000).toFixed(2)} s`;
};

export const formatConfidence = (confidence: number | null | undefined): string => {
  if (confidence === null || confidence === undefined) {
    return '-';
  }

  const normalized = confidence <= 1 ? confidence * 100 : confidence;
  return `${Math.round(normalized)}%`;
};

export const formatDateTime = (isoValue: string): string =>
  new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(isoValue));
