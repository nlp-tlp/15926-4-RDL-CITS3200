/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html', // If you have an index.html file in the root
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: { 
      // Extend or customize Tailwind's default theme
      colors: {
        // Map your CSS variables to Tailwind colors
        background: 'var(--color-background)',
        'background-soft': 'var(--color-background-soft)',
        'background-mute': 'var(--color-background-mute)',
        'nav-background': 'var(--color-nav-background)',
        'nav-text': 'var(--color-nav-text)',
        'nav-text-active': 'var(--color-nav-text-active)',
        'nav-title': 'var(--color-nav-title)',
        border: 'var(--color-border)',
        'border-hover': 'var(--color-border-hover)',
        heading: 'var(--color-heading)',
        text: 'var(--color-text)',
      },
      padding: {
        'section-gap-half': 'calc(var(--section-gap) / 2)',
      },
      margin: {
        'section-gap-half': 'calc(var(--section-gap) / 2)',
      },
    },
  },
  plugins: [],
}
