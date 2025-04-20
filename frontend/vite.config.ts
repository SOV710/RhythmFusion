import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// Automation Plugins
import AutoImport from 'unplugin-auto-import/vite'
import { VueRouterAutoImports } from 'unplugin-vue-router'
import Components from 'unplugin-vue-components/vite'
import VueRouter from 'unplugin-vue-router/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'

// Unocss kit
import UnoCSS from 'unocss/vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '127.0.0.1',
    port: 5173,
    open: true
  },

  plugins: [
    VueRouter({
      extensions: ['.vue', '.md'],
      dts: 'src/typed-router.d.ts',
    }),
    vue(),
    vueDevTools(),
    AutoImport({
      imports: [
        'vue',
        'vue-router',
        VueRouterAutoImports,
      ],
      resolvers: [
        ElementPlusResolver(),

        IconsResolver({
          prefix: 'Icon',
        })
      ],

      dts: 'src/auto-imports.d.ts',
    }),
    Components({
      extensions: ['vue', 'md'],
      include: [/\.vue$/, /\.vue\?vue/, /\.md$/],
      resolvers: [
        IconsResolver({
          enableCollections: ['ep', 'el'],
        }),

        ElementPlusResolver({
          importStyle: 'sass',
        })
      ],
      dts: 'src/components.d.ts',
    }),

    UnoCSS(),
    Icons({
      autoInstall: true,
    }),
  ],

  resolve: {
    alias: {
      '~': fileURLToPath(new URL('./src', import.meta.url)),
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "~/styles/element/index.scss" as *;`,
        api: 'modern-compiler',
      },
    },
  },

})
