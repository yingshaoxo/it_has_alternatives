import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { babel } from "@rollup/plugin-babel";

import { resolve } from 'path'

import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';

const pathResolve = (dir: string): any => resolve(__dirname, '.', dir)

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    babel({
      include: "src/prismjs.ts",
      plugins: [
        [
          "prismjs",
          {
            languages: "all",
            theme: "default",
            css: true,
          },
        ],
      ],
      babelHelpers: "bundled",
      extensions: [".js", ".jsx", ".es6", ".es", ".mjs", ".ts", "*.tsx"],
    }),
    // Components({
    //   resolvers: [AntDesignVueResolver()],
    // }),
  ],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        additionalData: `@import "${pathResolve('src')}/assets/less/variables.less";`
      }
    },
  },
})