import { Chip } from '@mui/material';

import type { EntityResponse } from '../../types/workflow';
import { titleCase } from '../../utils/format';

interface EntityCardProps {
  entities: EntityResponse;
}

const entityOrder: Array<keyof EntityResponse> = [
  'people',
  'organizations',
  'emails',
  'phones',
  'locations',
  'dates',
  'money',
  'skills',
  'technologies',
];

export const EntityCard = ({ entities }: EntityCardProps) => (
  <section className="bento-card p-8">
      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-brand">Extracted Data Objects</h2>
        <span className="rounded-full bg-surface-container px-3 py-1 text-xs font-bold text-muted">
          {entityOrder.reduce((count, key) => count + (entities[key]?.length ?? 0), 0)} Entities Found
        </span>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {entityOrder.map((key) => {
          const values = entities[key] ?? [];

          return (
            <section key={key} className="rounded-xl border border-line/70 bg-surface-low p-4">
              <h3 className="text-xs font-bold uppercase tracking-[0.12em] text-muted">{titleCase(key)}</h3>
              <div className="mt-3 flex flex-wrap gap-2">
                {values.length > 0 ? (
                  values.map((value) => <Chip key={value} label={value} size="small" />)
                ) : (
                  <span className="text-sm text-muted">-</span>
                )}
              </div>
            </section>
          );
        })}
      </div>
  </section>
);
