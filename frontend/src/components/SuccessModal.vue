<template>
  <!-- 弹窗遮罩层：半透明黑色背景，点击不关闭 -->
  <div class="modal-overlay">
    <!-- 弹窗容器：居中显示 -->
    <div class="modal-container">
      <!-- 弹窗头部：标题 -->
      <div class="modal-header">
        <h3 class="modal-title">操作结果</h3>
      </div>
      <!-- 弹窗内容：仅保留提示文本 -->
      <div class="modal-body">
        <p class="success-text">项目「{{ projectName }}」创建成功！</p>
      </div>
      <!-- 弹窗底部：确定按钮 -->
      <div class="modal-footer">
        <button
          class="confirm-btn"
          @click="handleConfirm"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SuccessModal',
  // 接收父组件传递的参数：项目名称、确定按钮回调
  props: {
    projectName: {
      type: String,
      required: true, // 必须传递项目名称，用于个性化提示
      default: '未命名项目'
    },
    onConfirm: {
      type: Function,
      required: true // 必须传递确定按钮的回调函数（用于跳转）
    }
  },
  methods: {
    // 点击确定按钮：触发父组件传递的回调
    handleConfirm() {
      this.onConfirm();
    }
  }
}
</script>

<style scoped>
/* 遮罩层：全屏覆盖，半透明 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100; /* 确保在所有内容之上 */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 弹窗容器：白色背景，圆角卡片 */
.modal-container {
  width: 90%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

/* 弹窗头部：浅灰色背景，标题居中 */
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

/* 弹窗内容：仅文本居中，调整内边距 */
.modal-body {
  padding: 32px 16px; /* 增加上下内边距，弥补移除图标后的空间 */
  text-align: center;
}

.success-text {
  margin: 0;
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
}

/* 弹窗底部：按钮居中 */
.modal-footer {
  padding: 12px 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

/* 确定按钮：绿色背景，hover效果 */
.confirm-btn {
  padding: 10px 24px;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.confirm-btn:hover {
  background-color: #359e75; /* hover加深绿色 */
}
</style>
