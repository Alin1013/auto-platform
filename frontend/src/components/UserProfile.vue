<template>
  <!-- 密码修改模态框 -->
  <div class="modal" v-if="showChangePwdModal" @click.self="showChangePwdModal = false">
    <div class="modal-content" @click.stop>
      <h3>修改密码</h3>
      <div class="modal-input-group">
        <label>当前密码：</label>
        <div class="password-input-wrapper">
          <input
            :type="showCurrentPwd ? 'text' : 'password'"
            v-model="currentPwd"
            class="modal-input"
            :disabled="isLoading"
          />
          <span class="toggle-btn" @click="showCurrentPwd = !showCurrentPwd">
            {{ showCurrentPwd ? '隐藏' : '显示' }}
          </span>
        </div>
      </div>
      <div class="modal-input-group">
        <label>新密码：</label>
        <div class="password-input-wrapper">
          <input
            :type="showNewPwd ? 'text' : 'password'"
            v-model="newPwd"
            class="modal-input"
            :disabled="isLoading"
          />
          <span class="toggle-btn" @click="showNewPwd = !showNewPwd">
            {{ showNewPwd ? '隐藏' : '显示' }}
          </span>
        </div>
      </div>
      <div class="modal-input-group">
        <label>确认新密码：</label>
        <div class="password-input-wrapper">
          <input
            :type="showConfirmPwd ? 'text' : 'password'"
            v-model="confirmPwd"
            class="modal-input"
            :disabled="isLoading"
          />
          <span class="toggle-btn" @click="showConfirmPwd = !showConfirmPwd">
            {{ showConfirmPwd ? '隐藏' : '显示' }}
          </span>
        </div>
      </div>
      <div class="modal-actions">
        <button @click="showChangePwdModal = false" class="cancel-btn" :disabled="isLoading">取消</button>
        <button @click="handleChangePassword" class="confirm-btn" :disabled="isLoading">
          {{ isLoading ? '修改中...' : '确认修改' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import request from "@/utils/request";

// 状态管理和路由实例
const store = useStore();
const router = useRouter();

// 密码显示状态
const showCurrentPwd = ref(false);
const showNewPwd = ref(false);
const showConfirmPwd = ref(false);

// 表单数据和状态
const showChangePwdModal = ref(false);
const currentPwd = ref('');
const newPwd = ref('');
const confirmPwd = ref('');
const isLoading = ref(false);


// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const response = await request.get('/core/user/me/');
    store.commit('UPDATE_USERNAME', response.data.username);
    store.commit('UPDATE_AVATAR', response.data.avatar);

  } catch (error) {
    console.error('获取用户信息失败:', error);
    // 若Token失效，跳转登录页
    if (error.response?.status === 401) {
      window.location.href = '/#/login';
    }
  }
};
onMounted(() => {
  fetchUserInfo();
})

// 密码修改处理
const handleChangePassword = async () => {
  // 表单验证
  if (!currentPwd.value.trim()) {
    alert('请输入当前密码');
    return;
  }
  if (newPwd.value.length < 8) {
    alert('新密码长度不能少于8位');
    return;
  }
  if (newPwd.value !== confirmPwd.value) {
    alert('两次输入的新密码不一致');
    return;
  }
  if (newPwd.value === currentPwd.value) {
    alert('新密码不能与当前密码相同');
    return;
  }

  isLoading.value = true;
  try {
    // 调用store中的密码修改方法
    const result = await store.dispatch('changePassword', {
      currentPwd: currentPwd.value,
      newPwd: newPwd.value
    });

    // 成功处理
    alert(result);
    currentPwd.value = '';
    newPwd.value = '';
    confirmPwd.value = '';
    showChangePwdModal.value = false;

    // 密码修改后跳转登录页重新登录
    setTimeout(() => {
      router.push('/login');
    }, 1000);
  } catch (error) {
    alert(error.message || '密码修改失败，请重试');
    console.error('密码修改失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// ESC键关闭模态框
const handleKeydown = (e) => {
  if (e.key === 'Escape' && showChangePwdModal.value) {
    showChangePwdModal.value = false;
  }
};

// 生命周期钩子
onMounted(() => {
  fetchUserInfo();
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
/* 模态框遮罩层 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 模态框内容 */
.modal-content {
  width: 90%;
  max-width: 500px;
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* 输入组样式 */
.modal-input-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.modal-input-group label {
  font-size: 14px;
  color: #333;
}

/* 密码输入容器 */
.password-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 输入框样式 */
.modal-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.modal-input:focus {
  outline: none;
  border-color: #3498db;
}

/* 显示/隐藏按钮 */
.toggle-btn {
  color: #3498db;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
  padding: 4px;
}

/* 按钮区域 */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

/* 取消按钮 */
.cancel-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  border-color: #999;
}

/* 确认按钮 */
.confirm-btn {
  padding: 8px 16px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.confirm-btn:hover {
  background-color: #2980b9;
}

/* 禁用状态 */
.confirm-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>