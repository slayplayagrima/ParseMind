import { Skeleton } from '@mui/material';

export const LoadingSkeleton = () => (
  <div className="space-y-4">
    <Skeleton variant="rounded" height={160} sx={{ borderRadius: '20px' }} />
    <div className="grid gap-4 md:grid-cols-3">
      <Skeleton variant="rounded" height={120} sx={{ borderRadius: '20px' }} />
      <Skeleton variant="rounded" height={120} sx={{ borderRadius: '20px' }} />
      <Skeleton variant="rounded" height={120} sx={{ borderRadius: '20px' }} />
    </div>
    <Skeleton variant="rounded" height={260} sx={{ borderRadius: '20px' }} />
  </div>
);
