import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';

export default defineConfig({
  output: {
    assetPrefix: '.', // i.e. turn absolute "/static" into relative "./static"
    distPath: {
      root: '../', // this was "dist" before
    },
  },
  plugins: [pluginReact()],
});
