import { Send } from 'lucide-react';

import { BrandMark } from '../common/BrandMark';

export const Footer = () => (
  <footer className="mt-20 border-t border-line bg-surface-low">
    <div className="mx-auto grid max-w-7xl gap-10 px-5 py-12 lg:grid-cols-4 lg:px-10">
      <div>
        <BrandMark compact />
        <p className="mt-5 max-w-xs text-sm leading-6 text-muted">
          Intellectual clarity through architectural precision. Processing complex documents with understated luxury.
        </p>
      </div>
      <div>
        <h4 className="mb-5 text-sm font-bold text-ink">Platform</h4>
        <ul className="space-y-3 text-sm text-muted">
          <li>Features</li>
          <li>API Reference</li>
          <li>Security</li>
          <li>Enterprise</li>
        </ul>
      </div>
      <div>
        <h4 className="mb-5 text-sm font-bold text-ink">Company</h4>
        <ul className="space-y-3 text-sm text-muted">
          <li>Privacy Policy</li>
          <li>Terms of Service</li>
          <li>Contact Support</li>
          <li>Status</li>
        </ul>
      </div>
      <div>
        <h4 className="mb-5 text-sm font-bold text-ink">Subscribe to Updates</h4>
        <div className="flex gap-2">
          <input
            aria-label="Email address"
            className="min-w-0 flex-1 rounded-lg border border-line bg-white px-4 py-2 text-sm outline-none focus:border-brand"
            placeholder="Email address"
            type="email"
          />
          <button className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand text-white" type="button">
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
    <div className="border-t border-line/70 px-5 py-6 text-center text-xs text-muted lg:px-10">
      © 2024 ParseMind. Intellectual clarity through architectural precision.
    </div>
  </footer>
);
