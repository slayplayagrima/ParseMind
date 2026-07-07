import { Chip } from '@mui/material';
import { Sparkles } from 'lucide-react';

import { EntityCard } from '../../cards/EntityCard';
import { MetadataCard } from '../../cards/MetadataCard';
import { RecommendationCard } from '../../cards/RecommendationCard';
import { SummaryCard } from '../../cards/SummaryCard';
import { Accordion } from '../../common/Accordion';
import { Table } from '../../tables/Table';
import type { ResumeWorkflowResult } from '../../../types/workflow';
import { fallback } from '../../../utils/format';

interface ResumeRendererProps {
  result: ResumeWorkflowResult;
}

export const ResumeRenderer = ({ result }: ResumeRendererProps) => {
  const { resume, entities } = result;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
      <div className="md:col-span-3">
        <SummaryCard title="Candidate" value={resume.candidate?.name} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Email" value={resume.candidate?.email} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Phone" value={resume.candidate?.phone} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Location" value={resume.candidate?.location} />
      </div>

      <section className="bento-card p-8 md:col-span-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-brand">
            <Sparkles size={18} />
            Candidate Summary
          </h2>
          <span className="rounded-full bg-[#fddfa8] px-3 py-1 text-xs font-bold text-[#261900]">AI SYNTHESIS</span>
        </div>
        <p className="text-base leading-7 text-muted">{fallback(resume.summary)}</p>
      </section>

      <div className="md:col-span-4">
        <MetadataCard
          title="Candidate"
          items={[
            { label: 'Name', value: resume.candidate?.name },
            { label: 'Email', value: resume.candidate?.email },
            { label: 'Phone', value: resume.candidate?.phone },
            { label: 'Location', value: resume.candidate?.location },
            { label: 'ATS Score', value: resume.ats_score },
          ]}
        />
      </div>

      <section className="bento-card p-8 md:col-span-6">
            <h2 className="mb-5 text-lg font-semibold text-brand">Education</h2>
            <Table
              columns={[
                { key: 'degree', label: 'Degree' },
                { key: 'institution', label: 'Institution' },
                { key: 'start_year', label: 'Start' },
                { key: 'end_year', label: 'End' },
              ]}
              rows={resume.education}
            />
      </section>

      <section className="bento-card p-8 md:col-span-6">
          <h2 className="mb-5 text-lg font-semibold text-brand">Experience</h2>
          <Accordion
            items={
              resume.experience.length > 0
                ? resume.experience.map((experience) => ({
                    title: `${fallback(experience.role)} at ${fallback(experience.company)}`,
                    content: (
                      <div className="space-y-2">
                        <p className="text-sm font-semibold text-ink">{fallback(experience.duration)}</p>
                        <p className="text-sm text-muted">{fallback(experience.description)}</p>
                      </div>
                    ),
                  }))
                : [{ title: '-', content: <p className="text-sm text-muted">-</p> }]
            }
          />
      </section>

      <section className="bento-card p-8 md:col-span-7">
          <h2 className="mb-5 text-lg font-semibold text-brand">Projects</h2>
          <Accordion
            items={
              resume.projects.length > 0
                ? resume.projects.map((project) => ({
                    title: project.name,
                    content: <p className="text-sm text-muted">{fallback(project.description)}</p>,
                  }))
                : [{ title: '-', content: <p className="text-sm text-muted">-</p> }]
            }
          />
      </section>

      <section className="bento-card p-8 md:col-span-5">
          <h2 className="text-lg font-semibold text-brand">Skills</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {resume.skills.length > 0 ? (
              resume.skills.map((skill) => <Chip key={skill} label={skill} />)
            ) : (
              <span className="text-sm text-muted">-</span>
            )}
          </div>
      </section>

      <div className="md:col-span-4">
        <RecommendationCard title="Certifications" recommendations={resume.certifications} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Strengths" recommendations={resume.strengths} />
      </div>
      <div className="md:col-span-4">
        <RecommendationCard title="Areas for Improvement" recommendations={resume.improvements} />
      </div>
      <div className="md:col-span-12">
        <EntityCard entities={entities} />
      </div>
    </div>
  );
};
