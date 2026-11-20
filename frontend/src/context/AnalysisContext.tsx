import { useCallback, useMemo, useState } from 'react';

import { analyzeDocument } from '../api/documents';
import type { AnalysisEnvelope } from '../types/workflow';
import { getErrorMessage } from '../utils/typeGuards';
import { AnalysisContext, type AnalysisContextValue } from './analysisContextValue';

export const AnalysisProvider = ({ children }: { children: React.ReactNode }) => {
  const [analysis, setAnalysis] = useState<AnalysisEnvelope | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);

  const analyzeFile = useCallback(async (file: File) => {
    setAnalysis(null);
    setError(null);
    setFileName(file.name);
    setProgress(0);
    setIsAnalyzing(true);

    try {
      const response = await analyzeDocument(file, { onProgress: setProgress });
      setAnalysis({
        fileName: file.name,
        analyzedAt: new Date().toISOString(),
        response,
      });
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  const clearAnalysis = useCallback(() => {
    setAnalysis(null);
    setError(null);
    setFileName(null);
    setProgress(0);
    setIsAnalyzing(false);
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const value = useMemo<AnalysisContextValue>(
    () => ({
      analysis,
      error,
      fileName,
      isAnalyzing,
      progress,
      analyzeFile,
      clearAnalysis,
      clearError,
    }),
    [analysis, analyzeFile, clearAnalysis, clearError, error, fileName, isAnalyzing, progress],
  );

  return <AnalysisContext.Provider value={value}>{children}</AnalysisContext.Provider>;
};
