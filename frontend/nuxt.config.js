module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'matrix-display-frontend',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Matrix Display Controller' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    },
    vendor: ['axios']
  },
  modules: [
    'bootstrap-vue/nuxt'
  ],
  plugins: [
    {src: '~/plugins/vue-sweetalert2', ssr: false},
    {src: '~/plugins/vue-flash-message', ssr: false}
  ],
  css: [
    'vue-flash-message/dist/vue-flash-message.min.css'
  ]
}

