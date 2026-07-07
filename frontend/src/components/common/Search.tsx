import { TextField } from '@mui/material';
import { Search as SearchIcon } from 'lucide-react';

interface SearchProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export const Search = ({ value, onChange, placeholder = 'Search' }: SearchProps) => (
  <TextField
    fullWidth
    value={value}
    placeholder={placeholder}
    onChange={(event) => onChange(event.target.value)}
    InputProps={{
      startAdornment: <SearchIcon className="mr-2 text-muted" size={18} />,
    }}
  />
);
