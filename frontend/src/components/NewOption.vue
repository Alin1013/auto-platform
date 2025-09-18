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
      selectedTestType: '', // 初始值为空字符串，与下拉选项value匹配
      projectName: ''       // 初始值为空字符串
    }
  },
  methods: {
    handleSubmit() {
      // 1. 严格校验表单：避免空值/空格提交
      const projectNameTrim = this.projectName.trim();
      if (!projectNameTrim) {
        alert('请输入有效的项目名称！');
        return;
      }
      if (!this.selectedTestType) {
        alert('请选择测试类型！');
        return;
      }

      // 2. 组装项目数据（字段必须与HomePage读取的一致）
      const newProject = {
        id: Date.now(), // 唯一ID（时间戳，确保不重复）
        name: projectNameTrim, // 去空格后的项目名
        testType: this.selectedTestType, // 如"apiTest"
        testTypeLabel: this.getTestTypeLabel(), // 如"接口测试"
        createTime: new Date().toLocaleString() // 本地化时间
      };

      // 3. 读取已有项目：必须用JSON.parse，且兜底空数组
      let existingProjects = localStorage.getItem('projects');
      // 关键：若localStorage中没有"projects"，初始化为空数组
      existingProjects = existingProjects ? JSON.parse(existingProjects) : [];

      // 4. 新增项目并重新存入：必须用JSON.stringify转换
      existingProjects.push(newProject);
      localStorage.setItem('projects', JSON.stringify(existingProjects));

      // 5. 调试验证：确认存储成功（打开F12→Application→LocalStorage查看）
      console.log('存储到localStorage的数据：', existingProjects);
      console.log('localStorage原始值：', localStorage.getItem('projects'));

      // 6. 跳转回首页（确保路径与HomePage的路由path一致）
      alert(`项目「${newProject.name}」创建成功！`);
      this.$router.push('/home');
    },

    // 确保测试类型中文标签正确生成（无undefined）
    getTestTypeLabel() {
      // 严格匹配下拉选项的value值
      const typeMap = {
        'apiTest': '接口测试',
        'uiTest': 'UI测试',
        'performanceTest': '性能测试'
      };
      // 兜底：若类型不匹配，返回"未知测试类型"（避免undefined）
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