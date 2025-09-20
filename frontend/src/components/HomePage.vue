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
            <!-- 修正：移除了重复的project-card嵌套 -->
            <div
              class="project-card"
              v-for="project in projects"
              :key="project.id"
              @click="handleCardClick(project)"
            >
              <div class="card-header">
                <span class="project-name">{{ project.name }}</span>
                <span class="project-type">{{ project.testTypeLabel }}</span>
              </div>
              <div class="card-footer">
                <span class="project-time">{{ project.createTime }}</span>
                <!-- 增加.stop修饰符防止事件冒泡 -->
                <button class="delete-btn" @click.stop="handleDeleteProject(project.id)">
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
      modalType: 'fail',      // 模态框显示的消息类型
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
    // 加载项目数据
    loadProjects() {
      try {
        const savedProjects = localStorage.getItem('projects');
        this.projects = savedProjects ? JSON.parse(savedProjects) : [];
      } catch (error) {
        this.projects = [];
        this.showModal('读取项目数据失败：' + error.message, 'fail');
        console.error('读取项目数据失败：', error);
      }
    },

    // 卡片点击事件处理
    handleCardClick(project) {
      // 判断测试类型是否为UI测试
      if (project.testType === 'uiTest') {
        // 跳转到UiInfo组件，并传递当前项目名称
        this.$router.push({
          path: '/UiInfo',
          query: { projectName: project.name }
        });
      }
      else if (project.testType==='apiTest'){
        //跳转到ApiInfo组件，并传递当前项目名称
        this.$router.push({
          path:'/ApiInfo',
          query: { projectName: project.name }
        });
      }
      else {
        this.showModal(`当前「${project.testTypeLabel}」类型暂不支持查看详情`, 'fail');
      }
    },

    // 新增项目按钮点击事件
    handleAddItem() {
      this.$router.push('/NewOption');
    },

    // 删除项目按钮点击事件
    handleDeleteProject(projectId) {
      // 暂存要删除的项目ID，获取项目名称
      this.deleteProjectId = projectId;
      const deleteProject = this.projects.find(p => p.id === projectId);
      const projectName = deleteProject ? deleteProject.name : '未命名项目';

      // 显示删除确认弹窗
      this.modalType = 'confirm';
      this.modalMessage = `确定要删除项目「${projectName}」吗？删除后不可恢复！`;
      this.modalVisible = true;
    },

    // 弹窗确认按钮回调
    handleModalConfirm() {
      // 只有确认删除类型才执行删除
      if (this.modalType === 'confirm' && this.deleteProjectId !== null) {
        try {
          const deleteProject = this.projects.find(p => p.id === this.deleteProjectId);
          const projectName = deleteProject ? deleteProject.name : '未命名项目';

          // 执行删除操作
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

    // 显示模态框
    showModal(message, type) {
      this.modalMessage = message;
      this.modalType = type;
      this.modalVisible = true;

      // 成功/失败弹窗自动关闭，确认弹窗需手动点击
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
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: 3rem;
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

/* 滚动容器样式 */
.project-scroll-container {
  width: 100%;
  overflow-x: auto; /* 允许横向滚动 */
  overflow-y: hidden; /* 隐藏纵向滚动 */
  padding: 8px 0;
  padding-bottom: 12px;
  min-height: 120px; /* 与项目卡片高度一致 */
  position: relative; /* 作为.no-project的定位参考 */
}

/* 自定义滚动条样式（Chrome/Safari） */
.project-scroll-container::-webkit-scrollbar {
  height: 8px; /* 滚动条高度 */
}

.project-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.project-scroll-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
  transition: background 0.3s;
}

.project-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Firefox滚动条样式 */
.project-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: #c1c1c1 #f1f1f1;
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
  transition: transform 0.3s, box-shadow 0.3s;
  text-align: center;
  position: relative;
  cursor: pointer; /* 显示指针表示可点击 */
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
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

/* 卡片底部样式 */
.card-footer {
  font-size: 0.8rem;
  color: #888;
  position: relative;
  padding: 4px 0;
  display: flex;
  justify-content: center; /* 时间戳水平居中 */
  align-items: center;
}

.project-time {
  text-align: center;
}

/* 无项目提示 */
.no-project {
  color: #888;
  font-size: 1rem;
  padding: 40px 20px;
  white-space: nowrap;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: inline-block;
  border-radius: 6px;
}

/* 添加项目按钮 */
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
  top: 50%;
  transform: translateY(-50%);
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.7rem;
  padding: 2px 8px;
  transition: background-color 0.2s;
  /* 提高层级确保可点击 */
  z-index: 5;
}

.delete-btn:hover {
  background-color: #d9363e;
  color: white;
}

/* 移除冗余样式 */
.delete-icon {
  display: none;
}
</style>
