import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve : {
    alias: {
        '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
  },
  test: {
    globals: true,
    environment: 'jsdom', // Virtuelle DOM-Umgebung für Vue-Komponenten
    include: ['src/**/*.test.js', 'src/**/*.test.ts'], // Alle Testdateien, auch für TypeScript
  },
});
