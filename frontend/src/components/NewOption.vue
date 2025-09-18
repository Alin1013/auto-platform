<template>
  <div class="new-option-container">
    <!-- 背景图片 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="新增选项页面背景" />
    </div>
    <!-- 标题 -->
    <h2 class="page-title">新增项目配置</h2>

    <!-- 中间表单容器 -->
    <div class="center-box">
      <div class="box-content">
        <h3>项目基础配置</h3>

        <!-- 项目表单 -->
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

    <!-- 成功弹窗：通过showModal控制显示/隐藏 -->
    <SuccessModal
      v-if="showModal"
      :project-name="projectName.trim()"
      :on-confirm="handleModalConfirm"
    />
  </div>
</template>

<script>
// 1. 引入弹窗组件
import SuccessModal from '@/components/SuccessModal.vue';

export default {
  name: 'NewOption',
  // 2. 注册弹窗组件
  components: {
    SuccessModal
  },
  data() {
    return {
      selectedTestType: '', // 测试类型
      projectName: '',      // 项目名称
      showModal: false      // 弹窗显示状态：默认隐藏
    }
  },
  methods: {
    // 表单提交逻辑
    handleSubmit() {
      const projectNameTrim = this.projectName.trim();
      // 表单校验
      if (!projectNameTrim || !this.selectedTestType) {
        alert('请完善项目名称和测试类型！');
        return;
      }

      // 组装项目数据并存储到localStorage
      const newProject = {
        id: Date.now(),
        name: projectNameTrim,
        testType: this.selectedTestType,
        testTypeLabel: this.getTestTypeLabel(),
        createTime: new Date().toLocaleString()
      };
      const existingProjects = JSON.parse(localStorage.getItem('projects') || '[]');
      existingProjects.push(newProject);
      localStorage.setItem('projects', JSON.stringify(existingProjects));

      // 3. 显示成功弹窗（替代原alert）
      this.showModal = true;
    },

    // 弹窗确定按钮回调：跳转回HomePage
    handleModalConfirm() {
      this.$router.push('/home');
    },

    // 获取测试类型中文标签
    getTestTypeLabel() {
      const typeMap = {
        apiTest: '接口测试',
        uiTest: 'UI测试',
        performanceTest: '性能测试'
      };
      return typeMap[this.selectedTestType] || '未知测试类型';
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