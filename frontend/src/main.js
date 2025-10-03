import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 创建 Vue 应用实例
const app = createApp(App)

// 全局注册 axios
app.config.globalProperties.$axios = axios;

// 安装路由和 Element Plus
app.use(router)
app.use(ElementPlus)

// 挂载到 DOM
app.mount('#app')