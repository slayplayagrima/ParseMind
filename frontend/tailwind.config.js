/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#faf9f7',
        surface: '#faf9f7',
        ink: '#1a1c1b',
        muted: '#44474d',
        cloud: '#f4f3f1',
        line: '#e6e2dd',
        outline: '#75777e',
        brand: '#0f1f39',
        'brand-container': '#25344f',
        secondary: '#4a6078',
        slate: '#617891',
        accent: '#d5b893',
        coffee: '#6f4d38',
        critical: '#632024',
        'surface-low': '#f4f3f1',
        'surface-container': '#efeeec',
        'surface-high': '#e9e8e6',
      },
      boxShadow: {
        soft: '0 4px 20px rgba(37, 52, 79, 0.04)',
        lift: '0 10px 30px rgba(37, 52, 79, 0.06)',
      },
      borderRadius: {
        brand: '20px',
      },
    },
  },
  plugins: [],
};
