import { beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from './client';
import { analyzeDocument } from './documents';

vi.mock('./client', () => ({
  apiClient: { post: vi.fn() },
}));

const post = vi.mocked(apiClient.post);
const file = new File(['%PDF-1.7'], 'contract.pdf', { type: 'application/pdf' });

describe('analyzeDocument', () => {
  beforeEach(() => {
    post.mockReset();
  });

  it('uploads the file as form data and returns the workflow result', async () => {
    const result = { metadata: { workflow: 'contract_workflow' }, result: {} };
    post.mockResolvedValue({ data: { success: true, data: result, error: null } });
    const onProgress = vi.fn();

    await expect(analyzeDocument(file, { onProgress })).resolves.toEqual(result);

    const [url, body] = post.mock.calls[0];
    expect(url).toBe('/analyze');
    expect((body as FormData).get('file')).toBe(file);
    expect(onProgress).toHaveBeenLastCalledWith(100);
  });

  it('reports upload progress, capped below 100 until the analysis returns', async () => {
    post.mockImplementation(async (_url, _body, config) => {
      config?.onUploadProgress?.({ loaded: 50, total: 100 } as never);
      config?.onUploadProgress?.({ loaded: 100, total: 100 } as never);
      return { data: { success: true, data: {}, error: null } };
    });
    const onProgress = vi.fn();

    await analyzeDocument(file, { onProgress });

    expect(onProgress.mock.calls.map(([value]) => value)).toEqual([50, 95, 100]);
  });

  it('throws the API error when the analysis fails', async () => {
    post.mockResolvedValue({ data: { success: false, data: null, error: 'Unsupported document.' } });

    await expect(analyzeDocument(file, { onProgress: vi.fn() })).rejects.toThrow(
      'Unsupported document.',
    );
  });
});
