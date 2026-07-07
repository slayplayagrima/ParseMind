import { motion } from 'framer-motion';
import { ArrowUpFromLine, CheckCircle2, Circle, FileSearch, GitBranch, Loader2, Upload } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Button } from '../../components/buttons/Button';
import { ErrorState } from '../../components/common/ErrorState';
import { EmptyState } from '../../components/common/EmptyState';
import { useAnalysis } from '../../context/AnalysisContext';

const loadingSteps = [
  'Uploading',
  'Extracting Text',
  'Detecting Document Type',
  'Selecting Workflow',
  'Running AI Skills',
  'Generating Structured Analysis',
  'Preparing Dashboard',
];

const stepDetails: Record<string, string> = {
  Uploading: 'Streaming document to secure cloud storage...',
  'Extracting Text': 'Reading and normalizing document text...',
  'Detecting Document Type': 'Classifying document structure...',
  'Selecting Workflow': 'Routing to the best analysis workflow...',
  'Running AI Skills': 'Executing specialized document skills...',
  'Generating Structured Analysis': 'Composing typed analysis output...',
  'Preparing Dashboard': 'Preparing the dashboard workspace...',
};

const stepIcons = [Upload, FileSearch, FileSearch, GitBranch, Loader2, Loader2, CheckCircle2];

export const LoadingPage = () => {
  const navigate = useNavigate();
  const { analysis, error, fileName, isAnalyzing, progress } = useAnalysis();
  const [elapsedSteps, setElapsedSteps] = useState(0);

  useEffect(() => {
    if (!isAnalyzing) {
      return undefined;
    }

    const interval = window.setInterval(() => {
      setElapsedSteps((current) => Math.min(current + 1, loadingSteps.length - 1));
    }, 900);

    return () => window.clearInterval(interval);
  }, [isAnalyzing]);

  useEffect(() => {
    if (analysis) {
      navigate('/analysis');
    }

    return undefined;
  }, [analysis, navigate]);

  const activeStep = useMemo(() => {
    if (analysis) {
      return loadingSteps.length - 1;
    }

    const progressStep = Math.floor((progress / 100) * (loadingSteps.length - 1));
    return Math.max(elapsedSteps, progressStep);
  }, [analysis, elapsedSteps, progress]);

  if (error) {
    return (
      <div className="px-4 py-16">
        <ErrorState
          title="Analysis failed"
          message={error}
          actionLabel="Upload Another Document"
          onAction={() => navigate('/upload')}
        />
      </div>
    );
  }

  if (!isAnalyzing && !analysis) {
    return (
      <div className="px-4 py-16">
        <EmptyState
          title="No analysis in progress"
          description="Upload a PDF to start document analysis."
          actionLabel="Go to Upload"
          onAction={() => navigate('/upload')}
        />
      </div>
    );
  }

  return (
    <div className="relative flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center overflow-hidden px-5 py-12">
      <div className="pointer-events-none absolute inset-0 opacity-50">
        <div className="absolute left-1/4 top-1/4 h-96 w-96 rounded-full bg-[#d7e3ff] blur-[120px]" />
        <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-[#e0c38e] blur-[120px]" />
      </div>

      <section className="relative z-10 w-full max-w-3xl">
        <div className="mb-12 flex flex-col items-center text-center">
          <div className="relative mb-8 flex h-48 w-48 items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, ease: 'linear', repeat: Infinity }}
              className="absolute inset-0 rounded-full border-2 border-brand/5 border-t-brand"
            />
            <div className="flex h-32 w-32 items-center justify-center rounded-full bg-brand/5 text-brand">
              <ArrowUpFromLine size={48} strokeWidth={1.8} />
            </div>
          </div>
          <h1 className="text-3xl font-bold tracking-[-0.01em] text-brand">
            {analysis ? 'Preparing Dashboard' : `${loadingSteps[activeStep]} Document`}
          </h1>
          <p className="mt-3 max-w-md text-lg text-muted">
            {fileName ? `${fileName} is moving through the ParseMind pipeline.` : 'Preparing your document for architectural analysis.'}
          </p>
        </div>

        <div className="bento-card relative overflow-hidden p-6">
          <div className="shimmer absolute inset-0 opacity-10" />
          <div className="relative">
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                {(() => {
                  const Icon = stepIcons[activeStep] ?? Loader2;
                  return <Icon className={analysis ? 'text-brand' : 'text-brand'} size={24} />;
                })()}
                <span className="text-xl font-semibold text-brand">{loadingSteps[activeStep]}</span>
              </div>
              <span className="rounded-full bg-brand-container px-4 py-1 text-xs font-bold uppercase tracking-[0.08em] text-[#b7c7e9]">
                {analysis ? 'Complete' : 'Active'}
              </span>
            </div>
            <div className="mb-3 h-1.5 overflow-hidden rounded-full bg-surface-container">
              <div className="h-full bg-brand transition-all duration-500" style={{ width: `${analysis ? 100 : progress}%` }} />
            </div>
            <div className="flex justify-between text-sm font-semibold text-muted">
              <span>{stepDetails[loadingSteps[activeStep]]}</span>
              <span>{analysis ? 100 : progress}%</span>
            </div>
          </div>
        </div>

        <div className="mt-5 grid gap-5 md:grid-cols-2">
          {[
            ['Foundation Layers', loadingSteps.slice(0, 3)],
            ['Intelligent Processing', loadingSteps.slice(3)],
          ].map(([title, steps]) => (
            <div key={title as string} className="rounded-xl border border-line bg-white/60 p-5 backdrop-blur-sm">
              <h3 className="mb-4 text-xs font-semibold uppercase tracking-[0.12em] text-muted">{title as string}</h3>
              <ul className="space-y-4">
                {(steps as string[]).map((step) => {
                  const index = loadingSteps.indexOf(step);
                  const isComplete = index < activeStep || Boolean(analysis);
                  const isActive = index === activeStep && !analysis;
                  const Icon = isComplete ? CheckCircle2 : isActive ? Loader2 : Circle;

                  return (
                    <li
                      key={step}
                      className={`flex items-center gap-3 transition ${
                        isActive || isComplete ? 'text-brand opacity-100' : 'text-muted opacity-50'
                      }`}
                    >
                      <Icon className={isActive ? 'animate-spin' : ''} size={18} />
                      <span className="text-sm">{step}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex items-center justify-center gap-3 text-sm font-semibold text-outline">
          <div className="h-px w-10 bg-line" />
          Intellectual Clarity
          <div className="h-px w-10 bg-line" />
        </div>

        {analysis ? (
          <div className="mt-8 flex justify-center">
            <Button variant="contained" onClick={() => navigate('/analysis')}>
              Open Dashboard
            </Button>
          </div>
        ) : null}
      </section>
    </div>
  );
};
