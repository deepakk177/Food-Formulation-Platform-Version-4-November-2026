/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.72rem', { lineHeight: '1rem' }],
        'xs': ['0.82rem', { lineHeight: '1.2rem' }],
        'sm': ['0.94rem', { lineHeight: '1.4rem' }],
        'base': ['1.05rem', { lineHeight: '1.6rem' }],
        'lg': ['1.2rem', { lineHeight: '1.75rem' }],
        'xl': ['1.35rem', { lineHeight: '1.9rem' }],
        '2xl': ['1.65rem', { lineHeight: '2.15rem' }],
        '3xl': ['2.05rem', { lineHeight: '2.45rem' }],
      },
      colors: {
        brand: {
          primary: '#164E3D',
          hover: '#123F32',
          secondary: '#4E7B67',
          background: '#F7F9F8',
          card: '#FFFFFF',
          border: '#E5E9E6',
          pill: '#ECF4F0',
          dark: '#191C1E',
          muted: '#5F6D67'
        }
      },
    },
  },
  plugins: [],
};
