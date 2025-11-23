import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite";
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'


export default defineConfig({
  base: '/', 
  build: {
    outDir: '../backend/dist', 
    emptyOutDir: true, 
    assetsDir: 'assets', 
  },
  
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(), 
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})