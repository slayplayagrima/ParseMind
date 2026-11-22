import { Alert, LinearProgress } from '@mui/material';
import {
  BarChart3,
  ChevronRight,
  Cloud,
  FileJson,
  FileText,
  Sparkles,
  UploadCloud,
} from 'lucide-react';
import { useCallback, useMemo, useState } from 'react';
import { type FileRejection, useDropzone } from 'react-dropzone';
import { useForm, useWatch } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

import { Button } from '../../components/buttons/Button';
import { StatusBadge } from '../../components/common/StatusBadge';
import { useAnalysis } from '../../context/useAnalysis';

// Matches the backend limit, which is set by Vercel's 4.5 MB request cap.
const MAX_UPLOAD_MB = 4;

const DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

// Matches the backend's supported types. The backend also checks the
// file's bytes, so this is only for fast feedback.
const ACCEPTED_TYPES = {
  'application/pdf': ['.pdf'],
  [DOCX_MIME]: ['.docx'],
  'text/plain': ['.txt'],
};

const ACCEPTED_EXTENSIONS = Object.values(ACCEPTED_TYPES).flat();

const UNSUPPORTED_MESSAGE = 'Only PDF, Word (.docx) and text (.txt) files are supported.';

const fileExtension = (name: string) => {
  const dot = name.lastIndexOf('.');
  return dot === -1 ? '' : name.slice(dot).toLowerCase();
};

interface UploadFormValues {
  file: File | null;
}

const fileFormats = [
  { label: 'PDF', icon: FileText, available: true },
  { label: 'DOCX', icon: FileText, available: true },
  { label: 'TXT', icon: FileText, available: true },
];

const recentHistory = [
  { name: 'Analysis history', meta: 'Coming Soon', tone: 'bg-[#cae2ff]' },
  { name: 'User profile', meta: 'Coming Soon', tone: 'bg-[#fddfa8]' },
];

export const UploadPage = () => {
  const navigate = useNavigate();
  const { analyzeFile, clearAnalysis, clearError, isAnalyzing, progress } = useAnalysis();
  const { control, setValue } = useForm<UploadFormValues>({
    defaultValues: {
      file: null,
    },
  });
  const selectedFile = useWatch({ control, name: 'file' });
  const [validationError, setValidationError] = useState<string | null>(null);

  const validateFile = useCallback((file: File): string | null => {
    if (!ACCEPTED_EXTENSIONS.includes(fileExtension(file.name))) {
      return UNSUPPORTED_MESSAGE;
    }

    if (file.size > MAX_UPLOAD_MB * 1024 * 1024) {
      return `File is too large. The limit is ${MAX_UPLOAD_MB} MB.`;
    }

    return null;
  }, []);

  const onDrop = useCallback(
    (acceptedFiles: File[], fileRejections: FileRejection[]) => {
      const [file] = acceptedFiles;
      clearError();

      if (!file) {
        // The dropzone filters by type before onDrop runs, so a rejected
        // file would otherwise be ignored without any feedback.
        if (fileRejections.length > 0) {
          setValidationError(UNSUPPORTED_MESSAGE);
        }
        return;
      }

      const error = validateFile(file);
      setValidationError(error);

      if (!error) {
        setValue('file', file, { shouldDirty: true, shouldValidate: true });
      }
    },
    [clearError, setValue, validateFile],
  );

  const { getInputProps, getRootProps, isDragActive } = useDropzone({
    accept: ACCEPTED_TYPES,
    maxFiles: 1,
    multiple: false,
    onDrop,
  });

  const canAnalyze = useMemo(() => Boolean(selectedFile) && !validationError && !isAnalyzing, [
    isAnalyzing,
    selectedFile,
    validationError,
  ]);

  const handleAnalyze = () => {
    if (!selectedFile || !canAnalyze) {
      return;
    }

    clearAnalysis();
    void analyzeFile(selectedFile);
    navigate('/loading');
  };

  return (
    <div className="mx-auto max-w-7xl px-5 py-16 lg:px-10">
      <header className="mb-16">
        <h1 className="max-w-3xl text-4xl font-bold tracking-[-0.02em] text-brand">
          Upload a professional document for AI-powered analysis.
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-8 text-secondary">
          High-fidelity extraction and structural analysis for contracts, resumes, invoices, reports and
          policies.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <section className="space-y-6 lg:col-span-8">
          <div className="bento-card p-6 sm:p-12">
            <div
              {...getRootProps()}
              className={`flex min-h-[420px] cursor-pointer flex-col items-center justify-center rounded-[20px] border-2 border-dashed p-8 text-center transition ${
                isDragActive ? 'border-brand bg-brand/5' : 'border-[#c5c6ce] hover:border-brand'
              }`}
            >
              <input {...getInputProps()} />
              <div className="mb-8 flex h-24 w-24 items-center justify-center rounded-full bg-surface-low text-brand transition group-hover:scale-105">
                <UploadCloud size={46} strokeWidth={1.8} />
              </div>
              <h2 className="text-xl font-medium text-brand">
                {isDragActive ? 'Drop your document here' : 'Drag and drop documents here'}
              </h2>
              <p className="mt-4 max-w-md text-muted">
                Limit {MAX_UPLOAD_MB} MB per file. PDF, Word (.docx) and text (.txt) files are supported.
              </p>
              <div className="mt-10 flex flex-col gap-4 sm:flex-row">
                <Button variant="contained" sx={{ minWidth: 150, px: 4, py: 1.4 }}>
                  Select File
                </Button>
                <Button disabled variant="outlined" startIcon={<Cloud size={17} />} sx={{ minWidth: 170, px: 4, py: 1.4 }}>
                  Cloud Import
                </Button>
              </div>
            </div>

            {selectedFile ? (
              <div className="mt-6 flex flex-col gap-3 rounded-xl border border-line bg-white p-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex min-w-0 items-center gap-3">
                  <FileJson className="shrink-0 text-brand" size={22} />
                  <div className="min-w-0">
                    <p className="truncate font-bold text-brand">{selectedFile.name}</p>
                    <p className="text-sm text-muted">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                </div>
                <StatusBadge label={`${fileExtension(selectedFile.name).slice(1).toUpperCase() || 'File'} selected`} tone="success" />
              </div>
            ) : null}

            {validationError ? (
              <Alert severity="error" className="mt-5">
                {validationError}
              </Alert>
            ) : null}

            {isAnalyzing ? (
              <div className="mt-6">
                <div className="mb-2 flex justify-between text-sm font-semibold text-muted">
                  <span>Upload progress</span>
                  <span>{progress}%</span>
                </div>
                <LinearProgress variant="determinate" value={progress} />
              </div>
            ) : null}
          </div>

          <div className="bento-card p-8">
            <label className="mb-6 block text-xs font-semibold uppercase tracking-[0.28em] text-secondary">
              Analysis Parameters
            </label>
            <div className="relative">
              <textarea
                className="h-36 w-full resize-none rounded-xl border-0 bg-surface-low p-5 text-sm leading-6 text-muted outline-none focus:ring-2 focus:ring-brand"
                placeholder="What should ParseMind look for? (e.g., 'Extract all liability clauses and identify inconsistencies with ISO 27001')"
              />
              <div className="absolute bottom-4 right-4 flex items-center gap-2 rounded-full border border-line/60 bg-white/70 px-3 py-1 text-xs text-muted backdrop-blur-sm">
                <Sparkles size={14} />
                AI Optimized
              </div>
            </div>
            <div className="mt-8 flex justify-end">
              <Button
                size="large"
                variant="contained"
                startIcon={<BarChart3 size={18} />}
                disabled={!canAnalyze}
                onClick={handleAnalyze}
                sx={{ minWidth: 260, py: 1.5 }}
              >
                Analyze Document
              </Button>
            </div>
          </div>
        </section>

        <aside className="space-y-6 lg:col-span-4">
          <div className="bento-card p-6">
            <h2 className="text-lg font-medium text-brand">File Formats</h2>
            <div className="mt-6 space-y-4">
              {fileFormats.map((format) => {
                const Icon = format.icon;

                return (
                  <div
                    key={format.label}
                    className={`flex items-center justify-between rounded-xl border p-3 ${
                      format.available ? 'border-brand/10 bg-surface-low' : 'border-line/70'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={format.available ? 'text-brand' : 'text-outline'} size={20} />
                      <span className={`font-medium ${format.available ? 'text-brand' : 'text-secondary'}`}>
                        {format.label}
                      </span>
                    </div>
                    <StatusBadge label={format.available ? 'Active' : 'Coming Soon'} tone={format.available ? 'info' : 'neutral'} />
                  </div>
                );
              })}
            </div>
          </div>

          <div className="bento-card p-6">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-lg font-medium text-brand">Recent History</h2>
              <button className="text-sm font-bold text-brand" type="button" disabled>
                View All
              </button>
            </div>
            <div className="space-y-4">
              {recentHistory.map((item) => (
                <div key={item.name} className="flex items-center gap-4 rounded-xl p-3 opacity-70">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${item.tone} text-brand`}>
                    <FileText size={18} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-brand">{item.name}</p>
                    <p className="text-xs text-muted">{item.meta}</p>
                  </div>
                  <ChevronRight className="text-outline" size={18} />
                </div>
              ))}
            </div>
          </div>

          <div className="bento-card relative h-40 overflow-hidden bg-brand-container p-6 text-white">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_rgba(213,184,147,0.35),_transparent_55%)]" />
            <div className="relative flex h-full flex-col justify-end">
              <p className="text-lg font-semibold">Precision Engineering</p>
              <p className="mt-1 text-sm text-white/75">Settings, profile, and reporting controls are staged for rollout.</p>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};
