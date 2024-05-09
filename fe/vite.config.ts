import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'

import AutoImport from 'unplugin-auto-import/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import Components from 'unplugin-vue-components/vite'
import { VueRouterAutoImports } from 'unplugin-vue-router'


import tailwind from "tailwindcss"
import autoprefixer from "autoprefixer"

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  plugins: [
    vue(),
    VueDevTools(),
    AutoImport({
      imports: ['vue', VueRouterAutoImports, 'vue/macros', '@vueuse/core'],
      dts: 'src/auto-imports.d.ts',
      dirs: [
        './src/composables/',
        './src/features/**/store',
        './src/features/**/composable',
      ],
      exclude: [/\.generated\.ts$/, /node_modules/],
    }),
    Components({
      dirs: ['src/components', 'src/features', 'src/views'],
      dts: 'src/components.d.ts',
      resolvers: [
        IconsResolver({
          prefix: 'i',
          enabledCollections: ['mdi'],
        }),
      ],
    }),
    // https://github.com/antfu/unplugin-icons
    Icons({
      autoInstall: true,
      compiler: 'vue3',
      scale: 1.5,
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
