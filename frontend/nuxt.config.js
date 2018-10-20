module.exports = {
  env: {
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8080'
  },
  /*
  ** Headers of the page
  */
  head: {
    title: 'RGB Matrix Display Controller',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'RGB Matrix Display Controller' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Bai+Jamjuree|Chakra+Petch|M+PLUS+1p|Open+Sans+Condensed:300|Titillium+Web'}
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
    vendor: ['axios', 'vue-color']
  },
  modules: [
    'bootstrap-vue/nuxt'
  ],
  plugins: [
    {src: '~/plugins/vue-sweetalert2', ssr: false},
    {src: '~/plugins/vue-flash-message', ssr: false},
    {src: '~/plugins/axios', ssr: false}
  ],
  css: [
    'vue-flash-message/dist/vue-flash-message.min.css'
  ]
}

