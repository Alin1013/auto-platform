<template>
  <div class="user-profile-container">
    <!-- 返回按钮 -->
    <button class="back-button" @click="handleBack">
      <i class="back-icon">←</i>
      <span>返回首页</span>
    </button>

    <!-- 用户资料卡片 -->
    <div class="profile-card">
      <!-- 头像区域（合并重复的头像容器） -->
      <div class="avatar-container">
        <img :src="avatarImg" alt="用户头像" class="avatar" />
        <button class="change-avatar-btn" @click="handleChangeAvatar">更换头像</button>
        <!-- 隐藏的文件输入框 -->
        <input
          type="file"
          ref="fileInput"
          class="hidden-file-input"
          accept="image/*"
          @change="handleFileSelect"
        >
      </div>

      <div class="user-info">
        <div class="info-item">
          <label>用户名：</label>
          <input
            type="text"
            v-model="username"
            class="info-input"
            :disabled="!isEditing"
          />
          <button
            class="edit-btn"
            @click="handleToggleEdit"
          >
            {{ isEditing ? '保存' : '编辑' }}
          </button>
        </div>

        <div class="info-item">
          <label>密码：</label>
          <button class="change-pwd-btn" @click="showChangePwdModal = true">修改密码</button>
        </div>
      </div>

      <!-- 退出登录按钮 -->
      <button class="logout-btn" @click="handleLogout">
        退出登录
      </button>
    </div>

    <!-- 密码修改模态框 -->
    <div class="modal" v-if="showChangePwdModal">
      <div class="modal-content">
        <h3>修改密码</h3>
        <div class="modal-input-group">
          <label>当前密码：</label>
          <input
            type="password"
            v-model="currentPwd"
            class="modal-input"
            :disabled="isLoading"
          />
        </div>
        <div class="modal-input-group">
          <label>新密码：</label>
          <input
            type="password"
            v-model="newPwd"
            class="modal-input"
            :disabled="isLoading"
          />
        </div>
        <div class="modal-input-group">
          <label>确认新密码：</label>
          <input
            type="password"
            v-model="confirmPwd"
            class="modal-input"
            :disabled="isLoading"
          />
        </div>
        <div class="modal-actions">
          <button @click="showChangePwdModal = false" class="cancel-btn" :disabled="isLoading">取消</button>
          <button @click="handleChangePassword" class="confirm-btn" :disabled="isLoading">
            {{ isLoading ? '修改中...' : '确认修改' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 提示消息 -->
    <div class="toast" v-if="showToast">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from "axios";
// 导入默认头像图片
import defaultAvatar from '@/assets/default-avatar.png';

// 状态管理和路由
const store = useStore();
const router = useRouter();

// 响应式变量
const username = ref('');
const currentPwd = ref('');
const newPwd = ref('');
const confirmPwd = ref('');
const isEditing = ref(false);
const showChangePwdModal = ref(false);
const showToast = ref(false);
const toastMessage = ref('');
const isLoading = ref(false);
const fileInput = ref(null);
// 头像使用响应式变量存储
const avatarImg = ref(defaultAvatar);
const isUploading = ref(false);

// 初始化用户信息
onMounted(() => {
  const userInfo = store.getters.getUserInfo;
  username.value = userInfo.username || '';
  // 从store获取用户头像（如果有）
  avatarImg.value = userInfo.avatar || defaultAvatar;
});

// 切换用户名编辑/保存状态
const handleToggleEdit = () => {
  if (isEditing.value) {
    if (username.value.trim()) {
      store.commit('UPDATE_USERNAME', username.value.trim());
      showToastMessage('用户名更新成功');
      isEditing.value = false;
    } else {
      showToastMessage('用户名不能为空');
    }
  } else {
    isEditing.value = true;
  }
};

// 返回首页
const handleBack = () => {
  router.push('/home').catch(err => {
    console.warn('路由跳转失败：', err);
  });
};

// 头像上传相关方法
const handleChangeAvatar = () => {
// 创建文件选择 input
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*'; // 只接受图片类型

  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 显示选中的图片预览
    const previewUrl = URL.createObjectURL(file);
    avatarImg.value = previewUrl;

    // 上传到本地接口
    try {
      isUploading.value = true;
      const formData = new FormData();
      formData.append('avatar', file);

      // 使用本地接口地址
      const response = await axios.post('http://localhost:8080/api/user/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          // 如果需要认证，添加token
          'Authorization': `Bearer ${store.state.token}`
        }
      });

      // 上传成功，更新Vuex中的头像地址
      if (response.data && response.data.avatarUrl) {
        store.commit('UPDATE_AVATAR', response.data.avatarUrl);
        showToastMessage('头像上传成功');
      }
    } catch (error) {
      console.error('头像上传失败:', error);
      // 上传失败，恢复默认头像
      avatarImg.value = store.state.userInfo.avatarUrl || defaultAvatar;
      showToastMessage('头像上传失败: ' + (error.response?.data?.message || error.message));
    } finally {
      isUploading.value = false;
      // 释放URL对象
      URL.revokeObjectURL(previewUrl);
    }
  };

  input.click();
};
// 页面加载时获取用户头像
onMounted(() => {
  const userInfo = store.getters.getUserInfo;
  username.value = userInfo.username || '';
  // 如果用户有头像，使用用户头像，否则使用默认头像
  avatarImg.value = userInfo.avatarUrl ? userInfo.avatarUrl : defaultAvatar;
});

const handleFileSelect = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    return showToastMessage('请选择图片文件');
  }

  // 验证文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    return showToastMessage('图片大小不能超过5MB');
  }

  // 预览并上传头像
  const reader = new FileReader();
  reader.onload = (event) => {
    // 先更新本地预览
    avatarImg.value = event.target.result;
    // 上传到服务器
    uploadAvatar(file);
  };
  reader.readAsDataURL(file);
};

const uploadAvatar = async (file) => {
  try {
    isLoading.value = true;
    const formData = new FormData();
    formData.append('avatar', file);

    // 调用上传接口
    await axios.post('/api/user/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    // 更新Vuex中的头像信息
    store.commit('UPDATE_AVATAR', avatarImg.value);
    showToastMessage('头像上传成功');
  } catch (error) {
    showToastMessage('头像上传失败，请重试');
    console.error('头像上传失败:', error);
  } finally {
    isLoading.value = false;
    // 清空文件输入，允许重复选择同一文件
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};

// 处理密码修改
const handleChangePassword = async () => {
  // 前端基础校验
  if (!currentPwd.value.trim()) {
    return showToastMessage('请输入当前密码');
  }
  if (!newPwd.value.trim()) {
    return showToastMessage('请输入新密码');
  }
  if (newPwd.value.trim() !== confirmPwd.value.trim()) {
    return showToastMessage('两次输入的新密码不一致');
  }
  if (newPwd.value.trim().length < 8) {
    return showToastMessage('新密码长度不能少于8位');
  }

  try {
    isLoading.value = true;
    const result = await store.dispatch('changePassword', {
      currentPwd: currentPwd.value.trim(),
      newPwd: newPwd.value.trim()
    });
    showChangePwdModal.value = false;
    showToastMessage(result || '密码修改成功');
    currentPwd.value = '';
    newPwd.value = '';
    confirmPwd.value = '';
  } catch (error) {
    showToastMessage(error.message || '密码修改失败，请重试');
  } finally {
    isLoading.value = false;
  }
};

// 处理退出登录
const handleLogout = async () => {
  try {
    isLoading.value = true;
    await store.dispatch('logoutAction');
    router.push('/login');
  } catch (error) {
    showToastMessage(error.message || '退出登录失败，请重试');
    isLoading.value = false;
  }
};

// 显示提示消息
const showToastMessage = (message) => {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

// 监听编辑状态取消时同步用户名
watch(isEditing, (newVal) => {
  if (!newVal) {
    const latestUserInfo = store.getters.getUserInfo;
    username.value = latestUserInfo.username || '';
  }
});
</script>

<style scoped>
/* 保持原有样式不变 */
.user-profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.back-button {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}
.back-button:hover {
  background-color: #e0e0e0;
}
.back-icon {
  margin-right: 6px;
}

.profile-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #f0f0f0;
  margin-bottom: 15px;
  display:block;
  margin-left: auto;
  margin-right: auto;
}
.change-avatar-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}
.change-avatar-btn:hover {
  background-color: #2980b9;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
}
.info-item label {
  width: 100px;
  font-size: 16px;
  color: #333;
}
.info-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}
.info-input:disabled {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.edit-btn, .change-pwd-btn {
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}
.edit-btn {
  background-color: #2ecc71;
  color: white;
  border: none;
}
.edit-btn:hover {
  background-color: #27ae60;
}
.change-pwd-btn {
  background-color: transparent;
  color: #3498db;
  border: 1px solid #3498db;
}
.change-pwd-btn:hover {
  background-color: #3498db;
  color: white;
}
.logout-btn {
  width: 100%;
  padding: 12px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}
.logout-btn:hover {
  background-color: #c0392b;
}
.logout-btn:disabled {
  background-color: #ec7063;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 24px;
}
.modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}
.modal-input-group {
  margin-bottom: 16px;
}
.modal-input-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
}
.modal-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}
.modal-input:disabled {
  background-color: #f9f9f9;
  cursor: not-allowed;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}
.cancel-btn, .confirm-btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}
.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: none;
}
.cancel-btn:hover {
  background-color: #e0e0e0;
}
.cancel-btn:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}
.confirm-btn {
  background-color: #3498db;
  color: white;
  border: none;
}
.confirm-btn:hover {
  background-color: #2980b9;
}
.confirm-btn:disabled {
  background-color: #85c1e9;
  cursor: not-allowed;
}

.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  z-index: 1001;
  animation: fadein 0.5s, fadeout 0.5s 2.5s;
}
.hidden-file-input{
  display: none;
}

@keyframes fadein {
  from { top: 0; opacity: 0; }
  to { top: 20px; opacity: 1; }
}
@keyframes fadeout {
  from { top: 20px; opacity: 1; }
  to { top: 0; opacity: 0; }
}
</style>