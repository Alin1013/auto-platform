const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 配置开发环境下的 API 代理，解决跨域问题
  devServer: {
    proxy: {
      // 匹配所有以 '/api' 开头的请求路径
      '/api': {
        target: 'http://localhost:8080',  // 后端 API 服务器地址
        changeOrigin: true,  // 允许跨域
        pathRewrite: {
          '^/api': '/api'  // 路径重写（保持原路径，因为后端接口已包含 '/api' 前缀）
        }
      }
    }
  }
})