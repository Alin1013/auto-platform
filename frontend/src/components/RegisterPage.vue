<template>
  <div class="register-container">
    <div class="register-form-wrapper">
      <div class="register-form">
        <div class="logo-title">
          <img src="@/assets/logo.png" alt="平台logo" class="logo" />
          <h2>账号注册</h2>
        </div>

        <el-form ref="registerForm" :model="form" :rules="rules" label-width="0px">
          <!-- 头像上传区域 -->
          <el-form-item>
            <div class="avatar-upload-wrapper">
              <div class="avatar-upload-container">
                <img :src="avatarUrl" alt="预览头像" class="avatar-preview" />
                <input
                  type="file"
                  class="avatar-upload-input"
                  accept="image/*"
                  @change="handleAvatarSelect"
                />
                <button type="button" class="upload-btn" @click="triggerFileSelect">
                  选择图片
                </button>
              </div>
            </div>
          </el-form-item>

          <!-- 其他表单内容保持不变 -->
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
              :type="showPassword ? 'text' : 'password'"
              v-model="form.password"
              placeholder="请输入密码"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
              <template #suffix>
                <el-icon @click="showPassword = !showPassword" style="cursor: pointer">
                  <EyeOff v-if="showPassword" />
                  <Eye v-else />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 确认密码 -->
          <el-form-item prop="confirmPassword">
            <el-input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="form.confirmPassword"
              placeholder="请确认密码"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
              <template #suffix>
                <el-icon @click="showConfirmPassword = !showConfirmPassword" style="cursor: pointer">
                  <EyeOff v-if="showConfirmPassword" />
                  <Eye v-else />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 操作按钮 -->
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="handleRegister">注册</el-button>
              <el-button @click="resetForm">重置</el-button>
            </div>
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
import { User, Lock, Eye, EyeOff } from '@element-plus/icons-vue';
import defaultAvatar from '@/assets/default-avatar.png';
import request from '@/utils/request';

export default {
  components: { User, Lock, Eye, EyeOff },
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
      avatarFile: null,
      showPassword: false,
      showConfirmPassword: false
    };
  },
  methods: {
    // 新增：触发文件选择器
    triggerFileSelect() {
      document.querySelector('.avatar-upload-input').click();
    },

    handleAvatarSelect(e) {
      const file = e.target.files[0];
      if (!file) return;

      // 验证图片类型和大小
      if (!file.type.startsWith('image/')) {
        this.$message.error('请选择图片文件');
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        this.$message.error('图片大小不能超过5MB');
        return;
      }

      this.avatarFile = file;
      const reader = new FileReader();
      reader.onload = (event) => {
        this.avatarUrl = event.target.result;
      };
      reader.readAsDataURL(file);
    },

    handleRegister() {
      this.$refs.registerForm.validate(async (valid) => {
        if (valid) {
          try {
            const formData = new FormData();
            formData.append('username', this.form.username);
            formData.append('password', this.form.password);
            if (this.avatarFile) {
              formData.append('avatar', this.avatarFile);
            }

            await request.post('/core/register/', formData, {
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
      this.showPassword = false;
      this.showConfirmPassword = false;
    },

    toLogin() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* 头像上传样式调整 */
.avatar-upload-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  margin: 0 auto;
}

.avatar-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px; /* 头像和按钮之间的间距 */
  margin: 0 auto;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
}

.upload-btn {
  padding: 8px 16px;
  border: 1px solid #409eff;
  color: #409eff;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.upload-btn:hover {
  background-color: #409eff;
  color: white;
}

/* 其他原有样式保持不变 */
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
  padding: 20px;
}

.register-form {
  width: 500px;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.logo-title {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  justify-content: center;
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.avatar-upload-input {
  display: none;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  width: 100%;
  margin-top: 20px;
}

.button-group .el-button {
  min-width: 140px;
  padding: 10px 0;
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}

.login-link span {
  color: #409eff;
  cursor: pointer;
  transition: color 0.3s;
}

.login-link span:hover {
  color: #1677ff;
  text-decoration: underline;
}

.el-input {
  height: 50px;
}

.el-input__wrapper {
  height: 100%;
}

.el-form-item {
  margin-bottom: 25px;
}
</style>