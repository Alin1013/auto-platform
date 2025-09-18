import { createRouter, createWebHashHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/components/HomePage.vue'
import NewOption from '@/components/NewOption.vue'
const router = createRouter({
  history: createWebHashHistory(), // 使用哈希路由
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/home',
      name: 'HomePage',
      component: HomePage
    },
      {
      path: '/NewOption',
      name: 'NewOption',
      component: NewOption
    }
  ]
})

export default router