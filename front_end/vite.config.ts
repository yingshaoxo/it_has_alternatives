import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';

const pathResolve = (dir: string): any => resolve(__dirname, '.', dir)

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    Components({
      resolvers: [AntDesignVueResolver()],
    }),
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