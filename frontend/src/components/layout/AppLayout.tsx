import { Outlet } from 'react-router-dom';

import { Footer } from './Footer';
import { Navbar } from '../navigation/Navbar';

export const AppLayout = () => (
  <div className="flex min-h-screen flex-col bg-background text-ink">
    <Navbar />
    <main className="flex-1">
      <Outlet />
    </main>
    <Footer />
  </div>
);
