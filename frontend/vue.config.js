module.exports = {
  css: {
    loaderOptions: {
      scss: {
        prependData: `@import "~@/assets/scss/variables.scss"; @import "~@/assets/scss/global.scss";`
      }
    }
  }
};
