import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import { AnalysisProvider } from '../../context/AnalysisContext';
import { UploadPage } from './UploadPage';

const renderPage = () => {
  const { container } = render(
    <MemoryRouter>
      <AnalysisProvider>
        <UploadPage />
      </AnalysisProvider>
    </MemoryRouter>,
  );

  return container.querySelector('input[type="file"]') as HTMLInputElement;
};

const pdf = (name: string, sizeInBytes = 1024) => {
  const file = new File(['%PDF-1.7'], name, { type: 'application/pdf' });
  Object.defineProperty(file, 'size', { value: sizeInBytes });
  return file;
};

describe('UploadPage', () => {
  it('shows the 4 MB limit', () => {
    renderPage();

    expect(screen.getByText(/Limit 4 MB per file/)).toBeInTheDocument();
  });

  it('accepts a PDF under the size limit', async () => {
    const input = renderPage();

    await userEvent.upload(input, pdf('contract.pdf'));

    expect(await screen.findByText('contract.pdf')).toBeInTheDocument();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('rejects a PDF over 4 MB before uploading it', async () => {
    const input = renderPage();

    await userEvent.upload(input, pdf('huge.pdf', 5 * 1024 * 1024));

    expect(await screen.findByRole('alert')).toHaveTextContent('File is too large. The limit is 4 MB.');
  });

  it('explains why a non-PDF file is rejected', async () => {
    const user = userEvent.setup({ applyAccept: false });
    const input = renderPage();

    await user.upload(input, new File(['hello'], 'notes.txt', { type: 'text/plain' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Only PDF files are supported.');
  });
});
