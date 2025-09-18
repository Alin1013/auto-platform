<template>
  <div class="login-container">
     <!-- 左侧插画部分 -->
    <div class="Login">
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
          <el-form-item>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-button type="primary" @click="handleLogin">登录</el-button>
              </el-col>
              <el-col :span="12">
                <el-button @click="resetForm">重置</el-button>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'

export default {
  name: 'LoginPage',
  components: { User, Lock }, // 注册图标组件
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          console.log('登录参数:', this.loginForm)
          this.$router.push('/home') // 路由跳转
        } else {
          console.log('表单验证失败')
        }
      })
    },
    resetForm() {
      this.$refs.loginForm.resetFields()
    }
  }
}
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
</style>