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
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      projects: []
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
        console.error('读取项目数据失败：', error);
      }
    },
    handleAddItem() {
      this.$router.push('/NewOption');
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
</style>
