const path = require("path");
module.exports = {
  configureWebpack: {
    devtool: "source-map",
    resolve: {
      alias: {
        vue: path.resolve("./node_modules/vue"),
        $assets: path.resolve("./src/assets/")
      }
    }
  },
  devServer: {
    overlay: {
      warnings: true,
      errors: true
    }
  },
  css: {
    loaderOptions: {
      scss: {
        prependData:
          '@import "~@/assets/scss/variables.scss"; @import "~@/assets/scss/global.scss";'
      }
    }
  },
  transpileDependencies: ["vuetify", "sbc-common-components"]
};
