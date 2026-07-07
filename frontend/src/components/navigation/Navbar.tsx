import { Button as MuiButton } from '@mui/material';
import { NavLink } from 'react-router-dom';

import { BrandMark } from '../common/BrandMark';

const navItems = [
  { label: 'Features', to: '/' },
  { label: 'Supported Documents', to: '/upload' },
  { label: 'Architecture', to: '/' },
  { label: 'API', to: '/' },
  { label: 'GitHub', to: '/' },
];

export const Navbar = () => (
  <header className="sticky top-0 z-50 h-16 border-b border-line bg-surface/80 shadow-sm backdrop-blur-md">
    <nav className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-5 lg:px-10">
      <NavLink to="/" aria-label="ParseMind home">
        <BrandMark compact />
      </NavLink>
      <div className="hidden items-center gap-8 md:flex">
        {navItems.map((item) => (
          <NavLink
            key={`${item.label}-${item.to}`}
            to={item.to}
            className={({ isActive }) =>
              `text-sm font-medium transition-colors ${
                isActive && item.to !== '/'
                  ? 'border-b-2 border-brand pb-1 text-brand'
                  : 'text-secondary hover:text-brand'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <MuiButton
          component={NavLink}
          to="/upload"
          variant="contained"
          sx={{ borderRadius: '9999px', px: 3, backgroundColor: '#0f1f39' }}
        >
          Analyze Document
        </MuiButton>
      </div>
    </nav>
  </header>
);
