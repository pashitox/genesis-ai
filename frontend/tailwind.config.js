/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { 
          500: '#8b5cf6', 
          600: '#7c3aed' 
        },
        accent: { 
          500: '#06b6d4',
          600: '#0891b2'
        },
        dark: { 
          900: '#0f172a', 
          800: '#1e293b',
          700: '#334155'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}