<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-container">
      <!-- 弹窗头部：标题根据类型切换 -->
      <div class="modal-header">
        <h3 class="modal-title">{{ type === 'success' ? '操作成功' : '操作失败' }}</h3>
      </div>
      <!-- 弹窗内容：图标颜色+文本根据类型切换 -->
      <div class="modal-body">
        <p class="modal-icon" :class="{ 'success-icon': type === 'success', 'fail-icon': type === 'fail' }">
          {{ type === 'success' ? '✓' : '×' }}
        </p>
        <p class="modal-text">{{ message }}</p>
      </div>
      <!-- 弹窗底部：确定按钮 -->
      <div class="modal-footer">
        <button class="confirm-btn" :class="{ 'success-btn': type === 'success', 'fail-btn': type === 'fail' }" @click="handleClose">
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FailModal',
  props: {
    // 控制显示/隐藏（必传）
    visible: {
      type: Boolean,
      required: true,
      default: false
    },
    // 提示消息（必传）
    message: {
      type: String,
      required: true,
      default: '操作异常'
    },
    // 弹窗类型：success（成功）/ fail（失败）（必传）
    type: {
      type: String,
      required: true,
      validator: val => ['success', 'fail'].includes(val) // 只允许两种类型
    }
  },
  methods: {
    // 点击确定按钮：触发close事件，通知父组件关闭
    handleClose() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
/* 遮罩层 */
.modal-overlay {
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

/* 弹窗容器 */
.modal-container {
  width: 90%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

/* 弹窗头部 */
.modal-header {
  padding: 16px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
}

.modal-title {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  text-align: center;
}

/* 弹窗内容 */
.modal-body {
  padding: 24px 16px;
  text-align: center;
}

.modal-icon {
  font-size: 2.5rem;
  margin: 0 0 12px;
}

/* 成功图标（绿色） */
.success-icon {
  color: #42b983;
}

/* 失败图标（红色） */
.fail-icon {
  color: #ff4d4f;
}

.modal-text {
  margin: 0;
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
}

/* 弹窗底部 */
.modal-footer {
  padding: 12px 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.confirm-btn {
  padding: 10px 24px;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* 成功按钮（绿色） */
.success-btn {
  background-color: #42b983;
}

.success-btn:hover {
  background-color: #359e75;
}

/* 失败按钮（红色） */
.fail-btn {
  background-color: #ff4d4f;
}

.fail-btn:hover {
  background-color: #d9363e;
}
</style>