import { createContext, useCallback, useContext, useMemo, useState } from 'react';

import { analyzeDocument } from '../api/documents';
import type { AnalysisEnvelope } from '../types/workflow';
import { getErrorMessage } from '../utils/typeGuards';

interface AnalysisContextValue {
  analysis: AnalysisEnvelope | null;
  error: string | null;
  fileName: string | null;
  isAnalyzing: boolean;
  progress: number;
  analyzeFile: (file: File) => Promise<void>;
  clearAnalysis: () => void;
  clearError: () => void;
}

const AnalysisContext = createContext<AnalysisContextValue | null>(null);

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

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);

  if (!context) {
    throw new Error('useAnalysis must be used inside AnalysisProvider.');
  }

  return context;
};
