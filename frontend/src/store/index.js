import { createStore } from 'vuex';
// 引入已安装的持久化插件
import createPersistedState from 'vuex-persistedstate';

// --------------------------
// 1. 初始化默认状态
// --------------------------
const DEFAULT_USER_INFO = {
  username: '1234567',
  avatar: '@/assets/user-avatar.png'
};

const DEFAULT_STATE = {
  userInfo: DEFAULT_USER_INFO,
  isLogin: true
};

// --------------------------
// 2. 创建 Store 实例
// --------------------------
const store = createStore({
  strict: process.env.NODE_ENV === 'development',

  state() {
    return { ...DEFAULT_STATE };
  },

  mutations: {
    UPDATE_USERNAME(state, newName) {
      if (typeof newName === 'string' && newName.trim()) {
        state.userInfo.username = newName.trim();
      }
    },

    UPDATE_AVATAR(state, avatarUrl) {
        state.userInfo.avatar = avatarUrl;
        localStorage.setItem('userInfo',JSON.stringify(state.userInfo));
    },

    LOGOUT(state) {
      state.userInfo = { ...DEFAULT_USER_INFO };
      state.isLogin = false;
    },

    LOGIN(state, userInfo) {
      state.isLogin = true;
      if (typeof userInfo === 'object' && userInfo !== null) {
        state.userInfo = { ...state.userInfo, ...userInfo };
      }
    }
  },

  actions: {
    // 修复1：用 _ 占位未使用的 commit，或在需要时使用
    async changePassword(_, { currentPwd, newPwd }) {
      // 修复2：使用 newPwd，解决未使用报错
      if (!currentPwd || !newPwd) {
        throw new Error('当前密码和新密码不能为空');
      }
      if (newPwd.length < 8) {
        throw new Error('新密码长度不能少于8位');
      }
      if (currentPwd === newPwd) {
        throw new Error('新密码不能与当前密码相同');
      }

      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        if (currentPwd === '123456') {
          return '密码修改成功，请重新登录';
        } else {
          throw new Error('当前密码错误，请重新输入');
        }
      } catch (error) {
        const errMsg = error instanceof Error ? error.message : '密码修改失败，请重试';
        throw new Error(errMsg);
      }
    },

    // 修复3：使用 commit，避免未使用报错
    async logoutAction({ commit }) {
      try {
        await new Promise(resolve => setTimeout(resolve, 500));
        commit('LOGOUT'); // 触发 mutation，使用 commit
      } catch (error) {
        throw new Error('退出登录失败，请重试');
      }
    }
  },

  getters: {
    getUserInfo(state) {
      return { ...state.userInfo };
    },

    getLoginStatus(state) {
      return state.isLogin;
    },

    getFormattedUsername(state) {
      return state.userInfo.username.trim() || '未登录用户';
    },

    getAvatarUrl(state) {
      return state.userInfo.avatar || '@/assets/default-avatar.png';
    }
  },

  // 配置持久化插件（依赖已安装）
  plugins: [
    createPersistedState({
      paths: ['userInfo', 'isLogin'], // 只持久化必要状态
      storage: window.localStorage,   // 存储到 localStorage
      key: 'vuex-user-state'          // 自定义存储键名
    })
  ]
});

// 封装挂载方法
export function setupStore(app) {
  app.use(store);
}

export default store;