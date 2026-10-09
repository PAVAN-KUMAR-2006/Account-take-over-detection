/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'navy': '#0A1128',
        'near-black': '#050814',
        'dark-blue': '#101C42',
        'subtle-cyan': '#00E5FF',
        'safe': '#10B981',
        'info': '#3B82F6',
        'warning': '#F59E0B',
        'suspicious': '#F97316',
        'critical': '#EF4444',
        'ai': '#8B5CF6'
      }
    },
  },
  plugins: [],
}
