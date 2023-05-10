import { defineConfig } from "vite";
import liveReload from "vite-plugin-live-reload";

export default defineConfig({
  plugins: [
    liveReload('../project/json/*.json')
  ]
})
