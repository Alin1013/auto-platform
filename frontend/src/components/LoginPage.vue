<template>
  <div class="login-container">
    <!-- 左侧插画部分 -->
    <div class="illustration">
      <img src="@/assets/Login.png" alt="登录插画" />
    </div>
    <div class="login-form-wrapper">
      <div class="login-form">
        <div class="logo-title">
          <!-- 右侧logo部分 -->
          <img src="@/assets/logo.png" alt="平台logo" class="logo" />
          <h2>自动化测试平台</h2>
        </div>
        <el-form ref="loginForm" :model="loginForm" :rules="loginRules" label-width="0px">
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="使用账号"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              type="password"
              v-model="loginForm.password"
              placeholder="密码"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <!-- 按钮区域：登录和注册按钮居中展示 -->
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="handleLogin">登录</el-button>
              <el-button type="success" @click="toRegister">注册</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      }
    };
  },
  setup() {
    return {
      router: useRouter()
    };
  },
  methods: {
    async handleLogin() {
      try {
        const res = await request.post('/core/token/', this.loginForm);
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh);
        this.router.push('/home');
      } catch (err) {
        this.$message.error('用户名或密码错误');
      }
    },
    async handleRegister() {
      try {
        await request.post('/core/register/', this.loginForm);
        this.$message.success('注册成功，请登录');
      } catch (err) {
        this.$message.error('注册失败');
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
}
.illustration {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f2f5;
}
.illustration img {
  max-width: 80%;
  max-height: 80%;
}
.login-form-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-form {
  width: 400px;
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.logo-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

/* 按钮组样式：实现居中展示 */
.button-group {
  display: flex;
  justify-content: center;
  gap: 15px; /* 按钮之间的间距 */
  width: 100%;
}

/* 按钮样式调整，确保大小一致 */
.button-group .el-button {
  min-width: 120px;
}
</style>