<template>
  <div class="new-option-container">
    <!-- 背景图片 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="新增选项页面背景" />
    </div>

    <!-- 顶部标题：保持原有顶部居中 -->
    <h2 class="page-title">新增项目配置</h2>

    <!-- 中间表单容器 -->
    <div class="center-box">
      <div class="box-content">
        <!-- 1. 新增：标题容器（包裹返回按钮 + 项目基础配置标题） -->
        <div class="title-wrapper">
          <button class="back-btn" @click="handleGoBack">◀返回</button>
          <h3>项目基础配置</h3>
        </div>

        <!-- 项目表单 -->
        <form class="config-form" @submit.prevent="handleSubmit">
          <div class="form-item">
            <label class="form-label">测试类型</label>
            <select v-model="selectedTestType" class="form-control" required>
              <option :value="''" disabled>请选择测试类型</option>
              <option value="apiTest">接口测试</option>
              <option value="uiTest">UI测试</option>
            </select>
          </div>
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
          <button type="submit" class="submit-btn">
            <span>确认创建</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 成功弹窗 -->
    <SuccessModal
      v-if="showModal"
      :project-name="projectName.trim()"
      :on-confirm="handleModalConfirm"
    />
  </div>
</template>

<script>
import SuccessModal from '@/components/SuccessModal.vue';

export default {
  name: 'NewOption',
  components: { SuccessModal },
  data() {
    return {
      selectedTestType: '',
      projectName: '',
      showModal: false
    }
  },
  methods: {
    handleGoBack() {
      this.$router.push('/home');
    },
    handleSubmit() {
      const projectNameTrim = this.projectName.trim();
      if (!projectNameTrim || !this.selectedTestType) {
        alert('请完善项目名称和测试类型！');
        return;
      }
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
      this.showModal = true;
    },
    handleModalConfirm() {
      this.$router.push('/home');
    },
    getTestTypeLabel() {
      const typeMap = { apiTest: '接口测试', uiTest: 'UI测试' };
      return typeMap[this.selectedTestType] || '未知测试类型';
    }
  }
}
</script>

<style scoped>
.new-option-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
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
  align-items: center; /* 让标题容器整体居中 */
  justify-content: center;
  gap: 28px; /* 标题容器与表单的间距 */
}

/* 3标题容器：控制返回按钮在左上角，标题居中 */
.title-wrapper {
  width: 100%; /* 占满box-content宽度，确保标题能居中 */
  display: flex;
  align-items: center; /* 按钮与标题垂直对齐 */
  position: relative; /* 作为返回按钮的定位参考 */
}

/* 返回按钮：固定在标题容器左上角 */
.back-btn {
  position: absolute;
  left: 0; /* 容器最左侧 */
  top: 50%;
  transform: translateY(-50%); /* 垂直居中 */
  background: transparent;
  border: none;
  color: #333;
  font-size: 1rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}
.back-btn:hover {
  background-color: rgba(245, 245, 245, 0.8);
}

/* 5项目基础配置标题：在标题容器内居中 */
.title-wrapper h3 {
  margin: 0;
  color: #555;
  font-size: 1.5rem;
  width: 100%; /* 占满容器宽度 */
  text-align: center; /* 文字居中 */
}

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

</style>