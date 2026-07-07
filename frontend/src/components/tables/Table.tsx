import {
  Table as MuiTable,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';

import { fallback } from '../../utils/format';

export interface Column<T> {
  key: keyof T;
  label: string;
  render?: (row: T) => React.ReactNode;
}

interface TableProps<T> {
  columns: Column<T>[];
  rows: T[];
  emptyLabel?: string;
}

const renderCellValue = (value: unknown): string => {
  if (typeof value === 'string' || typeof value === 'number') {
    return fallback(value);
  }

  if (value === null || value === undefined) {
    return fallback(value);
  }

  return String(value);
};

export const Table = <T extends object>({
  columns,
  rows,
  emptyLabel = '-',
}: TableProps<T>) => (
  <TableContainer className="rounded-xl border border-line/60">
    <MuiTable size="small">
      <TableHead className="bg-surface-low">
        <TableRow>
          {columns.map((column) => (
            <TableCell key={String(column.key)} className="font-bold text-ink">
              {column.label}
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.length > 0 ? (
          rows.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {columns.map((column) => (
                <TableCell key={String(column.key)}>
                  {column.render ? column.render(row) : renderCellValue(row[column.key])}
                </TableCell>
              ))}
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={columns.length} align="center" className="text-muted">
              {emptyLabel}
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </MuiTable>
  </TableContainer>
);
