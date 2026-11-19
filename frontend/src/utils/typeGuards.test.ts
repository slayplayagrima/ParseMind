import { describe, expect, it } from 'vitest';

import type { WorkflowResponse } from '../types/workflow';
import { getErrorMessage, hasContractResult, hasResumeResult } from './typeGuards';

const response = (result: unknown) => ({ metadata: {}, result }) as unknown as WorkflowResponse;

describe('result type guards', () => {
  it('recognises contract and resume results', () => {
    expect(hasContractResult(response({ contract: {}, entities: {} }))).toBe(true);
    expect(hasResumeResult(response({ resume: {}, entities: {} }))).toBe(true);
  });

  it('rejects results of the other type', () => {
    expect(hasContractResult(response({ resume: {} }))).toBe(false);
    expect(hasResumeResult(response(null))).toBe(false);
  });
});

describe('getErrorMessage', () => {
  it('prefers the error message sent by the API', () => {
    const error = { response: { status: 400, data: { success: false, error: 'PDF has 80 pages.' } } };

    expect(getErrorMessage(error)).toBe('PDF has 80 pages.');
  });

  it('falls back to a message for the status code', () => {
    expect(getErrorMessage({ response: { status: 429 } })).toMatch(/Too many requests/);
    expect(getErrorMessage({ response: { status: 503 } })).toMatch(/temporarily unavailable/);
  });

  it('uses the error message when there is no response', () => {
    expect(getErrorMessage(new Error('timeout of 120000ms exceeded'))).toBe(
      'timeout of 120000ms exceeded',
    );
  });

  it('has a generic message for anything else', () => {
    expect(getErrorMessage('boom')).toMatch(/network error/);
  });
});
