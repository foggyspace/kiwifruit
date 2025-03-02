import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  },
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:9527',
        changeOrigin: true
      }
    }
  }
})
