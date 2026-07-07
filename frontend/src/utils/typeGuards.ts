import type {
  ContractWorkflowResult,
  ResumeWorkflowResult,
  WorkflowResponse,
} from '../types/workflow';

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null;

export const hasContractResult = (
  response: WorkflowResponse,
): response is WorkflowResponse<ContractWorkflowResult> =>
  isRecord(response.result) && isRecord(response.result.contract);

export const hasResumeResult = (
  response: WorkflowResponse,
): response is WorkflowResponse<ResumeWorkflowResult> =>
  isRecord(response.result) && isRecord(response.result.resume);

export const getErrorMessage = (error: unknown): string => {
  if (isRecord(error)) {
    const response = error.response;
    if (isRecord(response)) {
      const data = response.data;
      if (isRecord(data)) {
        if (typeof data.detail === 'string') {
          return data.detail;
        }
        if (typeof data.error === 'string') {
          return data.error;
        }
      }
      if (typeof response.status === 'number') {
        if (response.status === 400) {
          return 'This document could not be analyzed. Please upload a supported PDF.';
        }
        if (response.status === 429) {
          return 'Too many requests. Please wait a moment and try again.';
        }
        if (response.status >= 500) {
          return 'The analysis service is temporarily unavailable. Please try again.';
        }
      }
    }
    if (typeof error.message === 'string') {
      return error.message;
    }
  }

  return 'A network error interrupted the analysis. Please check the backend and try again.';
};
