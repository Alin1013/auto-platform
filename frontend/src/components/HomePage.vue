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
                  删除
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

    <!-- 失败提示模态框 -->
    <FailModal
      :visible="modalVisible"
      :message="modalMessage"
      :type="modalType"
      @close="modalVisible = false"
      @confirm="handleModalConfirm"
    />
  </div>
</template>

<script>
import FailModal from '@/components/FailModal.vue';

export default {
  name: 'HomePage',
  components: {
    FailModal  // 注册组件
  },
  data() {
    return {
      projects: [],
      modalVisible: false,
      modalMessage: '',
      modalType: 'fail',      // 模态框显示的消息
      deleteProjectId: null
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
        this.showFailModal('读取项目数据失败：' + error.message);
        console.error('读取项目数据失败：', error);
      }
    },
    handleAddItem() {
      this.$router.push('/NewOption');
    },
handleDeleteProject(projectId) {
    // 1. 暂存要删除的项目ID，获取项目名称
    this.deleteProjectId = projectId;
    const deleteProject = this.projects.find(p => p.id === projectId);
    const projectName = deleteProject ? deleteProject.name : '未命名项目';

    // 2. 显示“删除确认弹窗”（type=confirm）
    this.modalType = 'confirm';
    this.modalMessage = `确定要删除项目「${projectName}」吗？删除后不可恢复！`;
    this.modalVisible = true;
  },

  // 新增：弹窗确认按钮的回调（删除逻辑移到这里）
  handleModalConfirm() {
    // 只有“确认删除”类型才执行删除
    if (this.modalType === 'confirm' && this.deleteProjectId !== null) {
      try {
        const deleteProject = this.projects.find(p => p.id === this.deleteProjectId);
        const projectName = deleteProject ? deleteProject.name : '未命名项目';

        // 执行删除
        this.projects = this.projects.filter(p => p.id !== this.deleteProjectId);
        localStorage.setItem('projects', JSON.stringify(this.projects));

        // 显示删除成功弹窗
        this.showModal(`项目「${projectName}」删除成功！`, 'success');
      } catch (error) {
        this.loadProjects();
        this.showModal('删除项目失败：' + error.message, 'fail');
        console.error('删除失败：', error);
      } finally {
        // 重置暂存的项目ID
        this.deleteProjectId = null;
      }
    }
  },

  // 修改showModal方法：保留自动关闭（仅成功/失败类型）
  showModal(message, type) {
    this.modalMessage = message;
    this.modalType = type;
    this.modalVisible = true;

    // 只有成功/失败弹窗自动关闭，确认弹窗需手动点击
    if (type === 'success' || type === 'fail') {
      setTimeout(() => {
        this.modalVisible = false;
      }, 3000);
    }
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
  position: relative;
  padding: 4px 0;
  display: flex;
  justify-content: center; /* 时间戳水平居中 */
  align-items: center;
}

/* 2. 时间戳：确保自身居中 */
.project-time {
  text-align: center;
}

.no-project {
  color: #888;
  font-size: 1rem;
  padding: 40px 20px;
  white-space: nowrap;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 基于自身中心点偏移，实现精准居中 */
  display: inline-block;
  border-radius: 6px;
}

.project-scroll-container {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 8px 0;
  padding-bottom: 12px;
  min-height: 120px; /* 与项目卡片高度一致，视觉统一 */
  position: relative; /* 作为.no-project的定位参考父级 */
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

/* 删除按钮样式：默认红底白字，hover可微调加深（可选） */
.delete-btn {
  position: absolute;
  right: 0;
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%);
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.7rem;
  padding: 2px 8px;
  transition: background-color 0.2s;
}

  .delete-btn:hover {
    background-color: #d9363e; /* 深红色hover效果 */
    color: white; /* 保持白色图标不变 */
  }

  .delete-icon {
    font-weight: normal; /* 取消加粗，避免图标过粗 */
    line-height: 1; /* 清除行高影响，确保垂直居中 */
  }
</style>
