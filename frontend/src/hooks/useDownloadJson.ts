import type { AnalysisEnvelope } from '../types/workflow';

export const useDownloadJson = () => {
  return (analysis: AnalysisEnvelope) => {
    const blob = new Blob([JSON.stringify(analysis.response, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `${analysis.fileName.replace(/\.pdf$/i, '') || 'analysis'}-analysis.json`;
    anchor.click();
    URL.revokeObjectURL(url);
  };
};
