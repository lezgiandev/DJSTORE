/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{vue,js,ts}'],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Светлая тема
                light: {
                    bg: '#ffffff',
                    'bg-secondary': '#f3f4f6',
                    'bg-tertiary': '#e5e7eb',
                    text: '#1f2937',
                    'text-secondary': '#4b5563',
                    border: '#e5e7eb',
                    'border-hover': '#d1d5db'
                }
            }
        }
    },
    plugins: [],
}