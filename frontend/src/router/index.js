import { createRouter, createWebHashHistory } from 'vue-router'
import LoginPage from '@/components/LoginPage.vue'
import HomePage from '@/components/HomePage.vue'
import NewOption from '@/components/NewOption.vue'
import SuccessModal from '@/components/SuccessModal.vue'
import FailModal from '@/components/FailModal.vue'
import UiInfo from '@/components/UiInfo.vue'
import ApiInfo from '@/components/ApiInfo.vue'
import RegisterPage from "@/components/RegisterPage.vue";


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
      },
      {
          path:'/UiInfo',
          name: 'UiInfo',
          component: UiInfo,
          props: route => ({
        currentProjectName: route.query.projectName
      })
      },
      {
          path:'/ApiInfo',
          name: 'ApiInfo',
          component: ApiInfo,
          props: route => ({
        currentProjectName: route.query.projectName
      })
      },
      {
          path:'/userprofile',
          name:'UserProfile',
          component: () => import ('@/components/UserProfile.vue'),
      },
      {
          path:'/register',
          name:'RegisterPage',
          component: RegisterPage
      }
  ]
});
router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('access_token');
  // 未登录用户禁止访问非登录/注册页面
  if (!isLogin && to.path !== '/login' && to.path !== '/register') {
    next('/login');
  } else {
    next();
  }
})
export default router