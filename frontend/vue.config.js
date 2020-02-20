module.exports = {
  transpileDependencies: ["vuetify"],
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "~@/assets/sass/variables.sass"`
      }
    }
  },
  devServer: {
    hot: false,
    liveReload: false
  }
};
