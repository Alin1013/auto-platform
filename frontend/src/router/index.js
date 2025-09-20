import { createRouter, createWebHashHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/components/HomePage.vue'
import NewOption from '@/components/NewOption.vue'
import SuccessModal from '@/components/SuccessModal.vue'
import FailModal from '@/components/FailModal.vue'

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
    },
      {
          path:'/SuccessModal',
          name: 'SuccessModal',
          component: SuccessModal
      },
      {
          path:'/FailModal',
          name: 'FailModal',
          component: FailModal
      }
  ]
})

export default router