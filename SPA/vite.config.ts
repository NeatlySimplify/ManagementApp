import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@auth": fileURLToPath(new URL("./src/features/auth", import.meta.url)),
      "@user": fileURLToPath(new URL("./src/features/user", import.meta.url)),
      "@entity": fileURLToPath(new URL("./src/features/entity", import.meta.url)),
      "@util": fileURLToPath(new URL("./src/util", import.meta.url)),
    },
  },
  build: {
    outDir: "../BackEnd/static", // change this to your desired output directory
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:3000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
