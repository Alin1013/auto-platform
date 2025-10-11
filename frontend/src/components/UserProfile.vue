<template>
  <!-- 密码修改模态框 -->
  <div class="modal" v-if="showChangePwdModal">
    <div class="modal-content">
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
// 导入ref
import { ref } from 'vue';

// 确保这些变量在模板中被使用
const showCurrentPwd = ref(false);
const showNewPwd = ref(false);
const showConfirmPwd = ref(false);

// 补充必要的响应式变量
const showChangePwdModal = ref(false);
const currentPwd = ref('');
const newPwd = ref('');
const confirmPwd = ref('');
const isLoading = ref(false);

// 补充处理函数
const handleChangePassword = async () => {
  // 实现密码修改逻辑
  isLoading.value = true;
  try {
    // 密码修改逻辑
    showChangePwdModal.value = false;
  } catch (error) {
    console.error('密码修改失败', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 保持样式不变 */
.password-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle-btn {
  color: #3498db;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.modal-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}
</style>