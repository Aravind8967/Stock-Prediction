import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:81/',
      '/ai' : 'http://localhost:83/'
    },
  },
  plugins: [react()],
})