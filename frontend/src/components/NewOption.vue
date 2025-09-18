<template>
  <div class="new-option-container">
    <!-- 标题文字 -->
    <h2 class="page-title">新增项目配置</h2>

    <!-- 中间方框容器：承载测试类型选择和项目名称输入 -->
    <div class="center-box">
      <div class="box-content">
        <h3>项目基础配置</h3>

        <!-- 表单区域 -->
        <form class="config-form" @submit.prevent="handleSubmit">
          <!-- 测试类型选择 -->
          <div class="form-item">
            <label class="form-label">测试类型</label>
            <select
              v-model="selectedTestType"
              class="form-control"
              required
            >
              <option :value="''" disabled>请选择测试类型</option>
              <option value="apiTest">接口测试</option>
              <option value="uiTest">UI测试</option>
              <option value="performanceTest">性能测试</option>
            </select>
          </div>

          <!-- 项目名称输入 -->
          <div class="form-item">
            <label class="form-label">项目名称</label>
            <input
              type="text"
              v-model="projectName"
              class="form-control"
              placeholder="请输入项目名称"
              required
            />
          </div>

          <!-- 提交按钮 -->
          <button type="submit" class="submit-btn">
            <i class="submit-icon">✓</i>
            <span>确认创建</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewOption',
  data() {
    return {
      // 绑定测试类型选择值
      selectedTestType: '',
      // 绑定项目名称输入值
      projectName: ''
    }
  },
  methods: {
    // 处理表单提交逻辑
    handleSubmit() {
      // 实际项目中可替换为接口请求（如调用后端创建项目接口）
      const configData = {
        testType: this.selectedTestType,
        projectName: this.projectName
      }
      console.log('项目配置提交数据：', configData)

      // 提交成功提示（后续可替换为路由跳转或弹窗反馈）
      alert(`项目创建成功！\n测试类型：${this.getTestTypeLabel()}\n项目名称：${this.projectName}`)

      // 重置表单
      this.selectedTestType = ''
      this.projectName = ''
    },
    // 辅助方法：根据选中的value获取测试类型中文标签
    getTestTypeLabel() {
      const typeMap = {
        apiTest: '接口测试',
        uiTest: 'UI测试',
        performanceTest: '性能测试'
      }
      return typeMap[this.selectedTestType] || ''
    }
  }
}
</script>

<style scoped>
/* 容器：占满整个视口，作为子元素定位参考 */
.new-option-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 背景图片：全屏底部固定，半透明效果 */
.bg-image {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.7;
}

.bg-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 页面标题：顶部居中，层级高于背景 */
.page-title {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: 2rem;
  color: #333;
}

/* 中间方框：居中显示，半透明白色背景 */
.center-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  width: 60%;
  max-width: 500px;
  min-height: 320px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 24px;
}

.box-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.box-content h3 {
  margin-bottom: 28px;
  color: #555;
  font-size: 1.5rem;
}

/* 表单样式 */
.config-form {
  width: 85%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-item {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.form-control {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
  outline: none;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

/* 提交按钮样式 */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 0;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #359e75;
}

.submit-icon {
  font-size: 1.1rem;
  font-weight: bold;
}
</style>