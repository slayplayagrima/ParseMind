import { useNavigate } from 'react-router-dom';

import { EmptyState } from '../../components/common/EmptyState';

export const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="px-4 py-16">
      <EmptyState
        title="Page not found"
        description="The page you are looking for does not exist."
        actionLabel="Return Home"
        onAction={() => navigate('/')}
      />
    </div>
  );
};
