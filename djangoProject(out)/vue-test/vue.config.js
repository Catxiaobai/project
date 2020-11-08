module.exports = {
  devServer: {
    port: 2333,
    open: true
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "@/assets/scss/_variable.scss";`
      }
    }
  }
  // proxyTable: {
  //   '/': {
  //     target: 'http://127.0.0.1:8000/',
  //     changeOrigin: true
  //   }
  // }
}
