// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://www.sapientjournal.com",
  integrations: [sitemap()],
  build: {
    // Keeps CSS inside the HTML so a single built page opens correctly on its own.
    inlineStylesheets: "always",
  },
});
