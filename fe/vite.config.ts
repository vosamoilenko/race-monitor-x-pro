import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'

import AutoImport from 'unplugin-auto-import/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import Components from 'unplugin-vue-components/vite'
import VueRouterAutoImports from 'unplugin-vue-router'


import tailwind from "tailwindcss"
import autoprefixer from "autoprefixer"

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  optimizeDeps: {
    include: [
      // "@fawmi/vue-google-maps",
      "vue-google-maps-community-fork",
      "fast-deep-equal",
    ],
  },
  plugins: [
    vue(),
    VueDevTools(),
    AutoImport({
      imports: [
        // Specifying as a simple string array if no renaming or specific imports are needed
        'vue',
        // For more complex modules, use an object to specify individual imports or settings
        {
          from: 'vue-router',
          imports: ['useRouter', 'useRoute'] // Specifying exact imports if needed
        },
        {
          from: 'vue/macros',
          imports: ['defineProps', 'defineEmits'] // Assume these are macros you need
        },
        '@vueuse/core' // This should work if this module does not require specific import handling
      ],
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
