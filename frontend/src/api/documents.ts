import { apiClient } from './client';
import type { APIResponse, WorkflowResponse } from '../types/workflow';

export interface AnalyzeOptions {
  onProgress: (progress: number) => void;
}

export const analyzeDocument = async (
  file: File,
  options: AnalyzeOptions,
): Promise<WorkflowResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<APIResponse<WorkflowResponse>>('/analyze', formData, {
    onUploadProgress: (event) => {
      if (!event.total) {
        options.onProgress(30);
        return;
      }

      options.onProgress(Math.min(95, Math.round((event.loaded / event.total) * 100)));
    },
  });

  if (!response.data.success || !response.data.data) {
    throw new Error(response.data.error ?? 'Analysis failed.');
  }

  options.onProgress(100);
  return response.data.data;
};
