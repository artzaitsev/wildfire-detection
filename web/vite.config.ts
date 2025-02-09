import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
import path from "node:path";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const envDir = path.resolve(__dirname, '..');
  const env = loadEnv(mode, envDir, '');
  return {
    define: Object.keys(env).reduce((acc, key) => {
      // @ts-ignore
      acc[`import.meta.env.${key}`] = JSON.stringify(env[key]);
      return acc;
    }, {}),
    plugins: [react(), tsconfigPaths()],
  }
})
