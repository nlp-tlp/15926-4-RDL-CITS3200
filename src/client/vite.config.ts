import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { defineConfig } from 'vitest/config'

// const path = require('path') // vitest config extends vite config

export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
      // '@/': path.resolve(__dirname, './src')
    }
  },
  test: {
    environment: 'jsdom',
    globals: true
  }
})
