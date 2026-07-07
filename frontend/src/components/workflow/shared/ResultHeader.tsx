import { Chip } from '@mui/material';
import { Calendar, Cpu, Download, FileDown, FileText, GitBranch, RotateCcw, Share2, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

import type { AnalysisEnvelope } from '../../../types/workflow';
import { formatConfidence, formatDateTime, formatMilliseconds, titleCase } from '../../../utils/format';
import { Button } from '../../buttons/Button';
import { StatusBadge } from '../../common/StatusBadge';
import { useDownloadJson } from '../../../hooks/useDownloadJson';

interface ResultHeaderProps {
  analysis: AnalysisEnvelope;
  onAnalyzeAnother: () => void;
}

export const ResultHeader = ({ analysis, onAnalyzeAnother }: ResultHeaderProps) => {
  const navigate = useNavigate();
  const downloadJson = useDownloadJson();
  const { metadata } = analysis.response;

  const handleAnalyzeAnother = () => {
    onAnalyzeAnother();
    navigate('/upload');
  };

  const metadataItems = [
    { label: 'Detected Document', value: analysis.fileName, icon: FileText },
    { label: 'Workflow Selected', value: `${titleCase(metadata.workflow)} Analysis`, icon: GitBranch },
    { label: 'Processing Time', value: formatMilliseconds(metadata.execution_time_ms), icon: Zap },
    { label: 'Confidence', value: formatConfidence(metadata.confidence), icon: null },
    { label: 'AI Model', value: metadata.model, icon: Cpu },
    { label: 'Analysis Date', value: formatDateTime(analysis.analyzedAt), icon: Calendar },
  ];

  return (
    <div>
      <header className="mb-8 flex flex-col justify-between gap-6 md:flex-row md:items-center">
        <div>
          <nav className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.12em] text-muted">
            <span>Workspace</span>
            <span>›</span>
            <span className="text-brand">Analysis Result</span>
          </nav>
          <h1 className="text-4xl font-bold tracking-[-0.02em] text-brand">Analysis Dashboard</h1>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button variant="outlined" startIcon={<RotateCcw size={17} />} onClick={handleAnalyzeAnother}>
            Analyze Another
          </Button>
          <Button variant="outlined" startIcon={<Download size={17} />} onClick={() => downloadJson(analysis)}>
            Download JSON
          </Button>
          <div className="relative">
            <Button disabled variant="outlined" startIcon={<FileDown size={17} />}>
              Download PDF Report
            </Button>
            <Chip className="absolute -right-2 -top-3" label="Coming Soon" size="small" />
          </div>
          <div className="relative">
            <Button disabled variant="outlined" startIcon={<Share2 size={17} />}>
              Share Report
            </Button>
            <Chip className="absolute -right-2 -top-3" label="Coming Soon" size="small" />
          </div>
        </div>
      </header>

      <section className="mb-8 flex flex-wrap items-center justify-between gap-4 rounded-[20px] border border-line/70 bg-white p-4 shadow-soft">
        <div className="flex min-w-0 flex-1 flex-wrap items-center gap-4 lg:gap-6">
          {metadataItems.map((item, index) => {
            const Icon = item.icon;

            return (
              <div key={item.label} className="flex min-w-[150px] items-center gap-2 border-line/60 pr-4 lg:border-r">
                {Icon ? <Icon className="shrink-0 text-secondary" size={18} /> : <span className="h-2.5 w-2.5 rounded-full bg-green-600" />}
                <div className="min-w-0">
                  <p className="mb-1 text-[10px] font-bold uppercase leading-none text-muted">{item.label}</p>
                  <p className={`truncate text-sm font-semibold ${index === 3 ? 'text-green-600' : 'text-ink'}`}>
                    {item.value}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
        <StatusBadge label={metadata.success ? 'Complete' : 'Incomplete'} tone={metadata.success ? 'success' : 'warning'} />
      </section>
    </div>
  );
};
