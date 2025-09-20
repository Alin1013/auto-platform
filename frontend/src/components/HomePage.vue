<template>
  <div class="home-container">
    <!-- 背景图片容器 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="主页面背景" />
    </div>
    <!-- 标题文字 -->
    <h1 class="page-title">项目</h1>

    <!-- 中间方框容器 -->
    <div class="center-box">
      <div class="box-content">
        <h3>项目区域</h3>

        <!-- 横向滑动容器：显示滚动条 -->
        <div class="project-scroll-container">
          <!-- 渲染已有的项目 -->
          <div class="project-list" v-if="projects.length > 0">
            <div class="project-card" v-for="project in projects" :key="project.id">
              <div class="card-header">
                <span class="project-name">{{ project.name }}</span>
                <span class="project-type">{{ project.testTypeLabel }}</span>
              </div>
              <div class="card-footer">
                <span class="project-time">{{ project.createTime }}</span>
                <button class="delete-btn" @click="handleDeleteProject(project.id)">
                  <i class="delete-icon">×</i>
                </button>
              </div>
            </div>
          </div>

          <!-- 无项目提示 -->
          <div class="no-project" v-else>
            暂无项目，点击下方按钮添加
          </div>
        </div>

        <!-- 添加新项目按钮 -->
        <button class="add-item-btn" @click="handleAddItem">
          <i class="add-icon">+</i>
          <span>添加新项目</span>
        </button>
      </div>
    </div>

    <!-- 弹窗组件：修复标签闭合 + 移除属性后注释 -->
    <FailModal
      :visible="modalVisible"
      :message="modalMessage"
      :type="modalType"
      @close="modalVisible = false"
    />
  </div>
</template>

<script>
import FailModal from '@/components/FailModal.vue';

export default {
  name: 'HomePage',
  components: { FailModal },
  data() {
    return {
      projects: [],
      // 合并弹窗状态（原 failModal 拆分为通用 modal 状态）
      modalVisible: false,   // 控制弹窗显示/隐藏
      modalMessage: '',      // 弹窗消息
      modalType: 'fail'      // 弹窗类型（默认失败，可选 success）
    }
  },
  mounted() {
    this.loadProjects();
  },
  watch: {
    $route() {
      this.loadProjects();
    }
  },
  methods: {
    loadProjects() {
      try {
        const savedProjects = localStorage.getItem('projects');
        this.projects = savedProjects ? JSON.parse(savedProjects) : [];
      } catch (error) {
        this.projects = [];
        // 调用失败提示（传递 type: 'fail'）
        this.showModal('读取项目数据失败：' + error.message, 'fail');
        console.error('读取项目数据失败：', error);
      }
    },
    handleAddItem() {
      this.$router.push('/NewOption');
    },
    handleDeleteProject(projectId) {
      // 1. 先获取当前要删除的项目名称（用于成功提示文案）
      const deleteProject = this.projects.find(p => p.id === projectId);
      const projectName = deleteProject ? deleteProject.name : '未命名项目';

      // 2. 确认删除
      if (confirm(`确定要删除项目「${projectName}」吗？`)) {
        try {
          // 3. 执行删除逻辑
          this.projects = this.projects.filter(project => project.id !== projectId);
          localStorage.setItem('projects', JSON.stringify(this.projects));

          // 4. 删除成功：调用成功提示（传递 type: 'success'）
          this.showModal(`项目「${projectName}」删除成功！`, 'success');
        } catch (error) {
          // 5. 删除失败：恢复数据并调用失败提示
          this.loadProjects();
          this.showModal('删除项目失败：' + error.message, 'fail');
          console.error('删除项目失败：', error);
        }
      }
    },
    // 新增：通用弹窗显示方法（支持成功/失败）
    showModal(message, type) {
      this.modalMessage = message;
      this.modalType = type;
      this.modalVisible = true;

      // 3秒后自动关闭（保持原有自动关闭逻辑）
      setTimeout(() => {
        this.modalVisible = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
/* 样式部分保持不变 */
.home-container {
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
  width: 80%;
  max-width: 1000px;
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
  justify-content: flex-start;
  gap: 24px;
}

.box-content h3 {
  margin: 0;
  color: #555;
  font-size: 1.5rem;
}

/*滚动条*/
.project-scroll-container {
  width: 100%;
  overflow-x: auto; /* 允许横向滚动 */
  overflow-y: hidden; /* 隐藏纵向滚动 */
  padding: 8px 0;
  padding-bottom: 12px;
}

/* 自定义滚动条样式（Chrome/Safari） */
.project-scroll-container::-webkit-scrollbar {
  height: 8px; /* 滚动条高度 */
}

/* 滚动条轨道 */
.project-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1; /* 轨道背景色 */
  border-radius: 10px; /* 轨道圆角 */
}

/* 滚动条滑块 */
.project-scroll-container::-webkit-scrollbar-thumb {
  background: #c1c1c1; /* 滑块颜色 */
  border-radius: 10px; /* 滑块圆角 */
  transition: background 0.3s;
}

/* 滑块hover效果 */
.project-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1; /* 滑块hover颜色加深 */
}

/* Firefox滚动条样式 */
.project-scroll-container {
  scrollbar-width: thin; /* 滚动条宽度：细 */
  scrollbar-color: #c1c1c1 #f1f1f1; /* 滑块颜色 轨道颜色 */
}

/* 横向项目列表 */
.project-list {
  display: flex;
  gap: 16px;
  width: max-content; /* 宽度自适应内容 */
  padding: 10px 0;
}

/* 项目卡片样式 */
.project-card {
  width: 280px;
  min-height: 120px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s;
  text-align: center;
  position: relative;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 12px; /* 增加间距，视觉更清晰 */
  align-items: center;
}

.project-name {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.project-type {
  font-size: 0.85rem;
  color: #fff;
  background-color: #42b983;
  padding: 3px 10px;
  border-radius: 12px;
}

.card-footer {
  font-size: 0.8rem;
  color: #888;
  text-align: right;
  position: relative;
  padding-right: 30px; /* 为删除按钮留出空间 */
}

.no-project {
  color: #888;
  font-size: 1rem;
  padding: 40px 20px;
  white-space: nowrap;
}

.add-item-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 8px;
}

.add-item-btn:hover {
  background-color: #359e75;
}

.add-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

/* 删除按钮样式 */
.delete-btn {
  position: absolute;
  right: 0;
  top: 0;
  background-color: transparent;
  border: none;
  color: #ff4d4f;
  cursor: pointer;
  font-size: 1rem;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.delete-btn:hover {
  background-color: #ff4d4f;
  color: white;
}

.delete-icon {
  font-weight: bold;
}
</style>
