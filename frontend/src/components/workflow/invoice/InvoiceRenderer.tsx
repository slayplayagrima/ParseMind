import { AlertTriangle, CheckCircle2, Sparkles } from 'lucide-react';

import { EntityCard } from '../../cards/EntityCard';
import { MetadataCard } from '../../cards/MetadataCard';
import { SummaryCard } from '../../cards/SummaryCard';
import { Table } from '../../tables/Table';
import type { InvoiceParty, InvoiceWorkflowResult } from '../../../types/workflow';
import { fallback, formatMoney } from '../../../utils/format';

interface InvoiceRendererProps {
  result: InvoiceWorkflowResult;
}

const partyItems = (party: InvoiceParty | undefined) => [
  { label: 'Name', value: party?.name },
  { label: 'Address', value: party?.address },
  { label: 'Email', value: party?.email },
  { label: 'Tax ID', value: party?.tax_id },
];

export const InvoiceRenderer = ({ result }: InvoiceRendererProps) => {
  const { invoice, entities } = result;
  const money = (value: number | null) => formatMoney(value, invoice.currency);
  const issues = invoice.issues ?? [];

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-12">
      <div className="md:col-span-3">
        <SummaryCard title="Invoice" value={invoice.invoice_number} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Total" value={money(invoice.total)} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Issued" value={invoice.issue_date} />
      </div>
      <div className="md:col-span-3">
        <SummaryCard title="Due" value={invoice.due_date} />
      </div>

      <section className="bento-card p-8 md:col-span-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-lg font-semibold text-brand">
            <Sparkles size={18} />
            Invoice Summary
          </h2>
          <span className="rounded-full bg-[#fddfa8] px-3 py-1 text-xs font-bold text-[#261900]">AI SYNTHESIS</span>
        </div>
        <p className="text-base leading-7 text-muted">{fallback(invoice.summary)}</p>
      </section>

      <section className="bento-card p-8 md:col-span-4" aria-label="Invoice checks">
        <h2 className="text-lg font-semibold text-brand">Checks</h2>
        <div className="mt-6 space-y-3">
          {issues.length === 0 ? (
            <div className="flex gap-3 rounded-xl border border-line/60 bg-surface-low p-4">
              <CheckCircle2 className="mt-0.5 shrink-0 text-green-700" size={18} />
              <p className="text-sm text-ink">All totals add up and the dates are consistent.</p>
            </div>
          ) : (
            issues.map((issue) => (
              <div key={issue} className="flex gap-3 rounded-xl border border-[#ffdad6] bg-[#fff4f2] p-4">
                <AlertTriangle className="mt-0.5 shrink-0 text-[#93000a]" size={18} />
                <p className="text-sm text-ink">{issue}</p>
              </div>
            ))
          )}
        </div>
      </section>

      <div className="md:col-span-4">
        <MetadataCard title="Vendor" items={partyItems(invoice.vendor)} />
      </div>
      <div className="md:col-span-4">
        <MetadataCard title="Bill To" items={partyItems(invoice.customer)} />
      </div>
      <div className="md:col-span-4">
        <MetadataCard
          title="Totals"
          items={[
            { label: 'Subtotal', value: money(invoice.subtotal) },
            { label: 'Tax', value: money(invoice.tax) },
            { label: 'Discount', value: money(invoice.discount) },
            { label: 'Total', value: money(invoice.total) },
            { label: 'Payment Terms', value: invoice.payment_terms },
          ]}
        />
      </div>

      <section className="bento-card p-8 md:col-span-12">
        <h2 className="mb-5 text-lg font-semibold text-brand">Line Items</h2>
        <Table
          columns={[
            { key: 'description', label: 'Description' },
            { key: 'quantity', label: 'Qty' },
            { key: 'unit_price', label: 'Unit Price', render: (row) => money(row.unit_price) },
            { key: 'amount', label: 'Amount', render: (row) => money(row.amount) },
          ]}
          rows={invoice.line_items}
        />
      </section>

      <div className="md:col-span-12">
        <EntityCard entities={entities} />
      </div>
    </div>
  );
};
