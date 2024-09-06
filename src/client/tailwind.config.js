/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html', // If you have an index.html file in the root
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: { // Extend or customize Tailwind's default theme
      colors: {
        background: 'var(--color-background)',
        text: 'var(--color-text)',
        // Add more if needed
      },
    },
  },
  plugins: [],
}
