import { createContext } from 'react';

import type { AnalysisEnvelope } from '../types/workflow';

export interface AnalysisContextValue {
  analysis: AnalysisEnvelope | null;
  error: string | null;
  fileName: string | null;
  isAnalyzing: boolean;
  progress: number;
  analyzeFile: (file: File) => Promise<void>;
  clearAnalysis: () => void;
  clearError: () => void;
}

export const AnalysisContext = createContext<AnalysisContextValue | null>(null);
