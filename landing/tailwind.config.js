/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f3ff',
          500: '#6366f1',
          600: '#4f46e5',
          900: '#312e81',
        }
      }
    },
  },
  plugins: [],
}
