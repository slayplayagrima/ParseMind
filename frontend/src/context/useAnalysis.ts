import { useContext } from 'react';

import { AnalysisContext } from './analysisContextValue';

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);

  if (!context) {
    throw new Error('useAnalysis must be used inside AnalysisProvider.');
  }

  return context;
};
