import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';

export default defineConfig({
  html: {
    template: './index_template.htm',
  },
  output: {
    assetPrefix: '.', // i.e. turn absolute "/static" into relative "./static"
    distPath: {
      root: '../', // this was "dist" before
    },
  },
  plugins: [pluginReact()],
});
