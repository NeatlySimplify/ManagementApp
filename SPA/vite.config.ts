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
      "@records": fileURLToPath(new URL("./src/features/records", import.meta.url)),
      "@util": fileURLToPath(new URL("./src/util", import.meta.url)),
      "@common": fileURLToPath(new URL("./src/features/common", import.meta.url)),
      "@movement": fileURLToPath(new URL("./src/features/movement", import.meta.url)),
      "@schedule": fileURLToPath(new URL("./src/features/schedule", import.meta.url)),
    },
  },
  build: {
    outDir: "../BackEnd/src/static", // change this to your desired output directory
  },
  server: {
    port: 5173,
  },
});
