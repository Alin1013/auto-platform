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
        <!-- 标题容器（包裹返回按钮 + 项目基础配置标题） -->
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
    async handleSubmit() {
      const projectNameTrim = this.projectName.trim();
      if (!projectNameTrim || !this.selectedTestType) {
        alert('请完善项目名称和测试类型！');
        return;
      }
      // 修复：将变量名从 newProject 改为 projectData（与接口调用处一致）
      const projectData = {
        name: projectNameTrim,
        test_type: this.selectedTestType,  // 匹配后端字段
        is_active: true  // 默认激活
      };
      try {
        // 修复：使用定义好的 projectData 变量
        const response = await this.$axios.post('http://localhost:8080/api/projects/', projectData);
        if (response.status === 201) {  // 创建成功
          this.showModal = true;
        }
      } catch (error) {
        console.error('创建项目失败：', error);
        alert('创建项目失败，请重试！');
      }
    },
    // 修复：将 handleModalConfirm 和 getTestTypeLabel 放入 methods 对象内
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
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: 2.5rem;
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
  align-items: center;
  justify-content: center;
  gap: 28px;
}

.title-wrapper {
  width: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
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

.title-wrapper h3 {
  margin: 0;
  color: #555;
  font-size: 1.5rem;
  width: 100%;
  text-align: center;
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