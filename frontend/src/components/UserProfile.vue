<template>
  <div class="user-profile-container">
    <!-- 返回按钮 -->
    <button class="back-button" @click="handleBack">
      <i class="back-icon">←</i>
      <span>返回首页</span>
    </button>

    <!-- 用户资料卡片 -->
    <div class="profile-card">
      <div class="avatar-container">
        <img :src="avatarImg" alt="用户头像" class="avatar" />
        <button class="change-avatar-btn" @click="handleChangeAvatar">更换头像</button>
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
// 修复1：导入缺失的 watch API
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
// 导入头像图片（确保 assets 目录下有该文件，无则替换为实际图片路径）
import avatarImg from '@/assets/user-avatar.png';

// 状态管理和路由
const store = useStore();
const router = useRouter();

// 响应式变量
const username = ref('');
const currentPwd = ref('');
const newPwd = ref('');
const confirmPwd = ref('');
const isEditing = ref(false); // 是否处于编辑状态（默认关闭）
const showChangePwdModal = ref(false); // 密码修改模态框显隐
const showToast = ref(false); // 提示消息显隐
const toastMessage = ref(''); // 提示消息内容
const isLoading = ref(false); // 加载状态（防止重复点击）

// 初始化用户信息（页面加载时从 Vuex 获取）
onMounted(() => {
  const userInfo = store.getters.getUserInfo;
  username.value = userInfo.username || '';
});

// 修复2：删除未使用的 handleSaveUsername，合并到切换编辑状态的逻辑中
// 切换用户名编辑/保存状态
const handleToggleEdit = () => {
  if (isEditing.value) {
    // 当前是“保存”状态：校验并更新用户名
    if (username.value.trim()) {
      store.commit('UPDATE_USERNAME', username.value.trim());
      showToastMessage('用户名更新成功');
      isEditing.value = false;
    } else {
      showToastMessage('用户名不能为空');
    }
  } else {
    // 当前是“编辑”状态：开启编辑
    isEditing.value = true;
  }
};

// 返回首页（跳转到 /home 路由，需确保路由配置中存在该路径）
const handleBack = () => {
  router.push('/home').catch(err => {
    // 捕获路由跳转错误（如已在首页）
    console.warn('路由跳转失败：', err);
  });
};

// 处理更换头像（模拟功能，实际项目需对接文件上传接口）
const handleChangeAvatar = () => {
  showToastMessage('头像更换功能待实现（需对接文件上传）');
  // 实际项目中可添加文件选择逻辑：
  // const input = document.createElement('input');
  // input.type = 'file';
  // input.accept = 'image/*';
  // input.onchange = (e) => { /* 处理上传逻辑 */ };
  // input.click();
};

// 处理密码修改（调用 Vuex 的 changePassword action）
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
    // 调用 Vuex action 修改密码（需确保 store 中已定义该 action）
    const result = await store.dispatch('changePassword', {
      currentPwd: currentPwd.value.trim(),
      newPwd: newPwd.value.trim()
    });
    // 修改成功：关闭模态框、清空输入、提示消息
    showChangePwdModal.value = false;
    showToastMessage(result || '密码修改成功');
    // 清空密码输入框
    currentPwd.value = '';
    newPwd.value = '';
    confirmPwd.value = '';
  } catch (error) {
    // 捕获错误并提示
    showToastMessage(error.message || '密码修改失败，请重试');
  } finally {
    // 无论成功失败，都关闭加载状态
    isLoading.value = false;
  }
};

// 处理退出登录（调用 Vuex 的 logoutAction，成功后跳转到登录页）
const handleLogout = async () => {
  try {
    isLoading.value = true;
    // 调用 Vuex action 执行退出逻辑（清除状态、调用后端登出接口等）
    await store.dispatch('logoutAction');
    // 退出成功：跳转到登录页（需确保路由配置中存在 /login 路径）
    router.push('/login');
  } catch (error) {
    // 退出失败：提示用户
    showToastMessage(error.message || '退出登录失败，请重试');
    isLoading.value = false;
  }
};

// 显示提示消息（3秒后自动消失）
const showToastMessage = (message) => {
  toastMessage.value = message;
  showToast.value = true;
  // 3秒后关闭提示
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

// 修复3：使用 watch 监听编辑状态（确保 watch 已导入）
// 当取消编辑时，从 Vuex 重新同步用户名（防止用户未保存直接取消）
watch(isEditing, (newVal) => {
  if (!newVal) {
    const latestUserInfo = store.getters.getUserInfo;
    username.value = latestUserInfo.username || '';
  }
});
</script>

<style scoped>
.user-profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 返回按钮样式 */
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

/* 资料卡片样式 */
.profile-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

/* 头像区域样式 */
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

/* 用户信息区域样式 */
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

/* 按钮样式 */
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

/* 模态框样式 */
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

/* 提示消息样式 */
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
/* 提示消息动画 */
@keyframes fadein {
  from { top: 0; opacity: 0; }
  to { top: 20px; opacity: 1; }
}
@keyframes fadeout {
  from { top: 20px; opacity: 1; }
  to { top: 0; opacity: 0; }
}
</style>