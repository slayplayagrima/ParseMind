import {
  AlertTriangle,
  ArrowRight,
  Badge,
  Braces,
  Building2,
  FileCheck2,
  FileText,
  Fingerprint,
  GitBranch,
  Gavel,
  Network,
  ReceiptText,
  Route,
  ShieldCheck,
  UploadCloud,
} from 'lucide-react';
import { Link } from 'react-router-dom';

import { Button } from '../../components/buttons/Button';

const capabilities = [
  {
    icon: Route,
    title: 'AI Router',
    description: 'Automatically detects document types and directs them to specialized extraction models.',
    wide: true,
  },
  {
    icon: AlertTriangle,
    title: 'Risk Detection',
    description: 'Flag contradictory clauses or missing information before analysis reaches the dashboard.',
  },
  {
    icon: GitBranch,
    title: 'Modular Workflows',
    description: 'Chain multiple workflow steps together for deep document context.',
  },
  {
    icon: Fingerprint,
    title: 'Entity Extraction',
    description: 'Isolate names, dates, amounts, skills, technologies, and professional entities.',
  },
  {
    icon: Braces,
    title: 'Structured Outputs',
    description: 'Render clean workflow responses and export backend JSON without inventing data.',
  },
];

const supportedHandlers = [
  { icon: Gavel, title: 'Contracts', description: 'Legal & procurement', active: true },
  { icon: Badge, title: 'Resumes', description: 'HR & recruiting', active: true },
  { icon: ReceiptText, title: 'Invoices', description: 'Finance & billing', active: false },
  { icon: FileText, title: 'Research', description: 'Academic & whitepapers', active: false },
  { icon: ShieldCheck, title: 'Medical', description: 'Coming Soon', active: false },
  { icon: Building2, title: 'Real Estate', description: 'Coming Soon', active: false },
];

export const LandingPage = () => (
  <div>
    <section className="hero-gradient overflow-hidden border-b border-line bg-surface py-20 lg:py-28">
      <div className="mx-auto grid max-w-7xl items-center gap-16 px-5 lg:grid-cols-2 lg:px-10">
        <div>
          <span className="mb-4 block text-xs font-semibold uppercase tracking-[0.28em] text-coffee">
            Architectural Intelligence
          </span>
          <h1 className="max-w-xl text-5xl font-bold leading-[1.08] tracking-[-0.02em] text-brand lg:text-6xl">
            Understand Any Document with AI
          </h1>
          <p className="mt-6 max-w-lg text-base leading-7 text-muted">
            Upload a professional document and receive structured AI-powered insights using specialized intelligent
            workflows designed for clarity and precision.
          </p>
          <div className="mt-10 flex flex-col gap-4 sm:flex-row">
            <Link to="/upload">
              <Button size="large" variant="contained" endIcon={<ArrowRight size={18} />} sx={{ px: 4, py: 1.5 }}>
                Analyze Document
              </Button>
            </Link>
            <Link to="/upload">
              <Button size="large" variant="outlined" sx={{ px: 4, py: 1.5, backgroundColor: '#ffffff' }}>
                Explore API
              </Button>
            </Link>
          </div>
        </div>

        <div className="relative min-h-[420px]">
          <svg className="absolute inset-0 h-full w-full" fill="none" viewBox="0 0 600 500">
            <path className="workflow-line" d="M95 250 C 205 250, 255 130, 430 110" stroke="#25344F" strokeOpacity="0.22" strokeWidth="2" />
            <path className="workflow-line" d="M95 250 C 205 250, 255 250, 430 250" stroke="#25344F" strokeOpacity="0.22" strokeWidth="2" />
            <path className="workflow-line" d="M95 250 C 205 250, 255 370, 430 390" stroke="#25344F" strokeOpacity="0.22" strokeWidth="2" />
          </svg>
          <div className="relative flex h-[420px] items-center justify-between">
            <div className="glass-card flex w-40 animate-[bounce_3s_infinite] flex-col items-center gap-3 rounded-[24px] p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-container text-white">
                <FileCheck2 size={22} />
              </div>
              <span className="text-xs font-bold uppercase text-brand">PDF / DOCX</span>
            </div>

            <div className="glass-card absolute left-1/2 top-1/2 z-20 flex h-32 w-32 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 shadow-lift">
              <div className="text-center">
                <Network className="mx-auto text-brand" size={36} />
                <span className="mt-1 block text-[10px] font-bold uppercase tracking-tight text-brand">AI Router</span>
              </div>
            </div>

            <div className="z-10 flex flex-col gap-10">
              {[
                ['Resume Parser', Badge, 'bg-[#e0c38e]'],
                ['Legal Contract', Gavel, 'bg-[#b7c7e9]'],
                ['Policy Analysis', ShieldCheck, 'bg-[#b1c9e5]'],
              ].map(([label, Icon, bg]) => (
                <div key={label as string} className="glass-card flex w-48 items-center gap-4 rounded-xl p-4">
                  <div className={`flex h-8 w-8 items-center justify-center rounded-md ${bg as string} text-brand`}>
                    <Icon size={16} />
                  </div>
                  <span className="text-sm font-semibold text-brand">{label as string}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section className="bg-surface py-24">
      <div className="mx-auto max-w-7xl px-5 lg:px-10">
        <div className="mb-16 text-center">
          <h2 className="text-4xl font-bold tracking-[-0.02em] text-brand">Precision-Engineered Features</h2>
          <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-muted">
            Our architecture is built for professional scale, ensuring every byte of your document is parsed with
            forensic clarity.
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
        {capabilities.map((capability) => {
          const Icon = capability.icon;

          return (
            <article key={capability.title} className={`glass-card rounded-[20px] p-8 ${capability.wide ? 'md:col-span-2' : ''}`}>
              <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-brand-container text-white">
                <Icon size={22} />
              </div>
              <h3 className="text-xl font-semibold text-brand">{capability.title}</h3>
              <p className="mt-3 text-sm leading-6 text-muted">{capability.description}</p>
            </article>
          );
        })}
          <article className="glass-card rounded-[20px] bg-brand-container p-8 text-white md:col-span-3">
            <div className="flex flex-col gap-8 md:flex-row md:items-center">
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-[#8e9dbd] text-brand">
                <ShieldCheck size={30} />
              </div>
              <div>
                <h3 className="text-xl font-semibold">Enterprise Ready Infrastructure</h3>
                <p className="mt-2 text-sm leading-6 text-[#b7c7e9]">
                  Deployment-ready frontend architecture with disabled placeholders for history, settings, profile, and
                  secure reporting features.
                </p>
              </div>
              <Button variant="contained" sx={{ ml: { md: 'auto' }, backgroundColor: '#ffffff', color: '#0f1f39', px: 3 }}>
                Request Security Whitepaper
              </Button>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section className="bg-white py-28">
      <div className="mx-auto max-w-5xl px-5 text-center lg:px-10">
        <h2 className="text-4xl font-bold tracking-[-0.02em] text-brand">The Architecture of Clarity</h2>
        <div className="mt-12 flex flex-col items-center justify-between gap-8 md:flex-row">
          {[
            ['01. Upload', UploadCloud, 'Drop PDFs into the workspace.'],
            ['02. AI Router', Network, 'Classification and workflow assignment.'],
            ['03. Results', FileCheck2, 'Structured data delivered to dashboard.'],
          ].map(([title, Icon, description], index) => (
            <div key={title as string} className="flex items-center gap-8 md:flex-1">
              <div className="flex w-48 flex-col items-center gap-4">
                <div className={`${index === 1 ? 'h-24 w-24 rounded-full bg-brand text-white' : 'h-20 w-20 rounded-2xl border border-line bg-white text-brand'} flex items-center justify-center shadow-soft`}>
                  <Icon size={index === 1 ? 34 : 28} />
                </div>
                <div>
                  <h4 className="font-bold text-brand">{title as string}</h4>
                  <p className="mt-1 text-xs leading-5 text-muted">{description as string}</p>
                </div>
              </div>
              {index < 2 ? <div className="hidden flex-1 border-t-2 border-dashed border-line md:block" /> : null}
            </div>
          ))}
        </div>
      </div>
    </section>

    <section className="bg-surface py-24">
      <div className="mx-auto max-w-7xl px-5 lg:px-10">
        <div className="mb-14 flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div>
            <h2 className="text-4xl font-bold tracking-[-0.02em] text-brand">Specialized Handlers</h2>
            <p className="mt-2 text-sm text-muted">Pre-trained intelligence for specific professional document categories.</p>
          </div>
          <button className="w-fit border-b-2 border-brand/10 pb-1 text-sm font-bold text-brand" type="button">
            Request Custom Model +
          </button>
        </div>
        <div className="grid grid-cols-2 gap-6 md:grid-cols-4">
          {supportedHandlers.map((handler) => {
            const Icon = handler.icon;
            return (
              <div key={handler.title} className={`bento-card flex flex-col items-center p-6 text-center ${handler.active ? '' : 'opacity-50'}`}>
                <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-surface-container text-brand">
                  <Icon size={24} />
                </div>
                <h4 className="font-bold text-brand">{handler.title}</h4>
                <p className="mt-1 text-xs text-muted">{handler.description}</p>
              </div>
            );
          })}
          <div className="flex flex-col items-center justify-center rounded-[20px] border border-dashed border-outline bg-surface-low p-6 text-center md:col-span-2">
            <span className="text-sm font-semibold text-secondary">More Coming Soon</span>
            <p className="mt-1 text-xs text-muted">We add new handlers based on user demand.</p>
          </div>
        </div>
      </div>
    </section>

    <section className="py-24">
      <div className="mx-auto max-w-5xl px-5 lg:px-10">
        <div className="relative overflow-hidden rounded-[40px] bg-brand p-12 text-center text-white md:p-20">
          <h2 className="mx-auto max-w-2xl text-4xl font-bold tracking-[-0.02em]">Ready to automate document clarity?</h2>
          <p className="mx-auto mt-6 max-w-2xl text-sm leading-6 text-[#b7c7e9]">
            Start analyzing documents today or integrate the API directly into your product workflow.
          </p>
          <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row">
            <Link to="/upload">
              <Button variant="contained" sx={{ backgroundColor: '#ffffff', color: '#0f1f39', px: 4 }}>
                Get Started Free
              </Button>
            </Link>
            <Button variant="outlined" sx={{ borderColor: 'rgba(255,255,255,0.25)', color: '#ffffff', px: 4 }}>
              Schedule Demo
            </Button>
          </div>
        </div>
      </div>
    </section>
  </div>
);
