// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js',
    exposeConfig: false,
    injectPosition: 0,
    viewer: false,
  },
  app: {
    baseURL: '/projects/shannon-insight/',
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.VITE_API_URL
    }
  }
})
