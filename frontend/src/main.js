import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import store from "./store";

// 创建应用实例
const app = createApp(App)

// 1. 配置全局属性（如 axios）
app.config.globalProperties.$axios = axios;

// 2. 安装插件
app.use(router)       // 路由
app.use(store)        // Vuex 状态管理
app.use(ElementPlus)  // UI组件库

// 3. 挂载到DOM
app.mount('#app')
