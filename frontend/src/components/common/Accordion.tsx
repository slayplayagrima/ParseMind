import {
  Accordion as MuiAccordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
} from '@mui/material';
import { ChevronDown } from 'lucide-react';

interface AccordionItem {
  title: string;
  content: React.ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
}

export const Accordion = ({ items }: AccordionProps) => (
  <div className="space-y-3">
    {items.map((item) => (
      <MuiAccordion
        key={item.title}
        disableGutters
        elevation={0}
        className="overflow-hidden rounded-xl border border-line/60 bg-surface-low"
      >
        <AccordionSummary expandIcon={<ChevronDown size={18} />}>
          <Typography className="font-bold text-ink">{item.title}</Typography>
        </AccordionSummary>
        <AccordionDetails>{item.content}</AccordionDetails>
      </MuiAccordion>
    ))}
  </div>
);
