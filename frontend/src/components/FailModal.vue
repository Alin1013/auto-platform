<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-container">
      <div class="modal-header">
        <h3 class="modal-title">{{ getTitle() }}</h3>
      </div>
      <div class="modal-body">
        <p class="modal-icon" :class="getIconClass()">
          {{ getIcon() }}
        </p>
        <p class="modal-text">{{ message }}</p>
      </div>
      <!-- 新增：根据类型显示“单按钮”或“双按钮” -->
      <div class="modal-footer" :class="{ 'two-btn': type === 'confirm' }">
        <!-- 取消按钮：仅确认类型显示 -->
        <button
          v-if="type === 'confirm'"
          class="cancel-btn"
          @click="handleCancel"
        >
          取消
        </button>
        <!-- 确认按钮：所有类型显示 -->
        <button
          class="confirm-btn"
          :class="getBtnClass()"
          @click="handleConfirm"
        >
          {{ type === 'confirm' ? '确认删除' : '确定' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FailModal',
  props: {
    visible: { type: Boolean, required: true, default: false },
    message: { type: String, required: true, default: '操作异常' },
    type: {
      type: String,
      required: true,
      validator: val => ['success', 'fail', 'confirm'].includes(val) // 新增confirm类型
    }
  },
  methods: {
    // 点击确认/确定按钮：触发confirm事件
    handleConfirm() {
      this.$emit('confirm');
      this.$emit('close'); // 关闭弹窗
    },
    // 点击取消按钮：仅触发close事件
    handleCancel() {
      this.$emit('close');
    },
    // 动态获取标题
    getTitle() {
      const titleMap = {
        success: '操作成功',
        fail: '操作失败',
        confirm: '确认删除'
      };
      return titleMap[this.type];
    },
    // 动态获取图标类名
    getIconClass() {
      const iconClassMap = {
        success: 'success-icon',
        fail: 'fail-icon',
        confirm: 'confirm-icon' // 新增确认类型图标类
      };
      return iconClassMap[this.type];
    },
    // 动态获取图标
    getIcon() {
      const iconMap = {
        success: '✓',
        fail: '×',
      };
      return iconMap[this.type];
    },
    // 动态获取按钮类名
    getBtnClass() {
      const btnClassMap = {
        success: 'success-btn',
        fail: 'fail-btn',
        confirm: 'confirm-btn' // 新增确认按钮类
      };
      return btnClassMap[this.type];
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

/* 确认图标（红色，区分成功/失败） */
.confirm-icon {
  color: #b61b1b;
}
/* 确认按钮 */
.confirm-btn {
  background-color: #b61b1b;
}
.confirm-btn:hover {
  background-color: #b61b1b;
}
/* 取消按钮样式 */
.cancel-btn {
  padding: 10px 24px;
  color: #333;
  background-color: #f5f5f5;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 12px;
  transition: background-color 0.3s;
}
.cancel-btn:hover {
  background-color: #e8e8e8;
}
/* 双按钮布局 */
.two-btn {
  justify-content: center;
  gap: 8px;
}
</style>