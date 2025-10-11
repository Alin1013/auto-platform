<template>
  <div class="register-container">
    <div class="register-form-wrapper">
      <div class="register-form">
        <div class="logo-title">
          <img src="@/assets/logo.png" alt="平台logo" class="logo" />
          <h2>账号注册</h2>
        </div>

        <el-form ref="registerForm" :model="form" :rules="rules" label-width="0px">
          <!-- 用户名 -->
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 密码 -->
          <el-form-item prop="password">
            <el-input
              type="password"
              v-model="form.password"
              placeholder="请输入密码"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 确认密码 -->
          <el-form-item prop="confirmPassword">
            <el-input
              type="password"
              v-model="form.confirmPassword"
              placeholder="请确认密码"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 头像上传 -->
          <el-form-item>
            <label class="avatar-upload-label">选择头像</label>
            <div class="avatar-upload-container">
              <img :src="avatarUrl" alt="预览头像" class="avatar-preview" />
              <input
                type="file"
                class="avatar-upload-input"
                accept="image/*"
                @change="handleAvatarSelect"
              />
              <button type="button" class="upload-btn">选择图片</button>
            </div>
          </el-form-item>

          <!-- 操作按钮 -->
          <el-form-item>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-button type="primary" @click="handleRegister">注册</el-button>
              </el-col>
              <el-col :span="12">
                <el-button @click="resetForm">重置</el-button>
              </el-col>
            </el-row>
          </el-form-item>

          <!-- 已有账号？去登录 -->
          <div class="login-link">
            已有账号？<span @click="toLogin">去登录</span>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue';
import defaultAvatar from '@/assets/default-avatar.png';
import request from "@/utils/request";

export default {
  components: { User, Lock },
  data() {
    return {
      form: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在3-20之间', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, message: '密码长度不能少于8位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.form.password) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ]
      },
      avatarUrl: defaultAvatar,
      avatarFile: null
    };
  },
  methods: {
    handleAvatarSelect(e) {
      const file = e.target.files[0];
      if (!file) return;

      this.avatarFile = file;
      const reader = new FileReader();
      reader.onload = (event) => {
        this.avatarUrl = event.target.result;
      };
      reader.readAsDataURL(file);
    },

    async handleRegister() {
      this.$refs.registerForm.validate(async (valid) => {
        if (valid) {
          try {
            const formData = new FormData();
            formData.append('username', this.form.username);
            formData.append('password', this.form.password);
            if (this.avatarFile) {
              formData.append('avatar', this.avatarFile);
            }

            // 调用注册接口
            await this.$axios.post('/core/register', formData, {
              headers: { 'Content-Type': 'multipart/form-data' }
            });

            this.$message.success('注册成功，请登录');
            this.toLogin();
          } catch (error) {
            this.$message.error(error.response?.data?.message || '注册失败，请重试');
          }
        }
      });
    },

    resetForm() {
      this.$refs.registerForm.resetFields();
      this.avatarUrl = defaultAvatar;
      this.avatarFile = null;
    },

    toLogin() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* 复用登录页样式并添加注册页特有样式 */
.register-container {
  display: flex;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-form-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-form {
  width: 400px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.logo-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  justify-content: center;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.avatar-upload-label {
  display: block;
  margin-bottom: 10px;
  color: #666;
}

.avatar-upload-container {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.avatar-preview {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
}

.avatar-upload-input {
  display: none;
}

.upload-btn {
  padding: 6px 12px;
  border: 1px solid #409eff;
  color: #409eff;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
}

.login-link {
  text-align: center;
  margin-top: 15px;
  color: #666;
  font-size: 14px;
}

.login-link span {
  color: #409eff;
  cursor: pointer;
}
</style>