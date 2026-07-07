import { useNavigate } from 'react-router-dom';

import { EmptyState } from '../../components/common/EmptyState';
import { ResultHeader } from '../../components/workflow/shared/ResultHeader';
import { WorkflowRenderer } from '../../components/workflow/shared/WorkflowRenderer';
import { useAnalysis } from '../../context/AnalysisContext';

export const AnalysisPage = () => {
  const navigate = useNavigate();
  const { analysis, clearAnalysis } = useAnalysis();

  if (!analysis) {
    return (
      <div className="px-4 py-16">
        <EmptyState
          title="No analysis available"
          description="Upload and analyze a PDF to view a workflow dashboard."
          actionLabel="Upload Document"
          onAction={() => navigate('/upload')}
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-5 py-8 lg:px-10">
      <ResultHeader analysis={analysis} onAnalyzeAnother={clearAnalysis} />
      <WorkflowRenderer response={analysis.response} />
    </div>
  );
};
