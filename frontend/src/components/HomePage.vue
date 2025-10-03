<template>
  <div class="home-container">
    <!-- 背景图片容器：修复图片路径解析问题 -->
    <div class="bg-image">
      <img :src="backgroundImg" alt="主页面背景" />
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
            <div
              class="project-card"
              v-for="project in projects"
              :key="project.id"
              @click="handleCardClick(project)"
            >
              <div class="card-header">
                <span class="project-name" :title="project.name">{{ project.name }}</span>
                <span class="project-type" :class="project.testType === 'apiTest' ? 'type-api' : 'type-ui'">
                  {{ project.testTypeLabel }}
                </span>
              </div>
              <div class="card-footer">
                <span class="project-time">{{ project.createTime }}</span>
                <!-- .stop 防止事件冒泡，避免点击删除时触发卡片跳转 -->
                <button
                  class="delete-btn"
                  @click.stop="handleDeleteProject(project.id, project.name)"
                  :disabled="isDeleting"
                >
                  {{ isDeleting && deleteingProjectId === project.id ? '删除中...' : '删除' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 无项目提示：优化文案和样式 -->
          <div class="no-project" v-else>
            <i class="no-project-icon">📂</i>
            <p>暂无项目</p>
            <p class="no-project-tip">点击下方「添加新项目」开始</p>
          </div>
        </div>

        <!-- 添加新项目按钮：增加加载状态 -->
        <button
          class="add-item-btn"
          @click="handleAddItem"
          :disabled="isNavigating"
        >
          <i class="add-icon">+</i>
          <span>{{ isNavigating ? '跳转中...' : '添加新项目' }}</span>
        </button>
      </div>
    </div>

    <!-- 失败提示模态框：统一处理成功/失败/确认场景 -->
    <FailModal
      :visible="modalVisible"
      :message="modalMessage"
      :type="modalType"
      :confirm-loading="isDeleting"
      @close="modalVisible = false"
      @confirm="handleModalConfirm"
    />
  </div>
</template>

<script>
// 导入背景图片（解决路径解析问题，适配Vue 2/3）
import backgroundImg from '@/assets/background.png';
import FailModal from '@/components/FailModal.vue';

export default {
  name: 'HomePage',
  components: { FailModal },
  data() {
    return {
      backgroundImg, // 挂载图片资源到data
      projects: [],
      modalVisible: false,
      modalMessage: '',
      modalType: 'fail', // 支持：fail/success/confirm
      deleteProjectId: null, // 暂存当前要删除的项目ID
      deleteingProjectId: null, // 正在删除的项目ID（用于加载状态）
      projectName: '', // 暂存当前要删除的项目名称
      isDeleting: false, // 删除操作加载状态
      isNavigating: false // 页面跳转加载状态
    }
  },
  mounted() {
    // 页面加载时自动获取项目列表
    this.loadProjects();
  },
  watch: {
    // 路由变化时重新加载项目（如从新增页面返回时）
    $route: {
      handler: 'loadProjects',
      immediate: false
    }
  },
  methods: {
    /**
     * 加载项目列表：修复接口数据解析，增加错误处理
     */
    async loadProjects() {
      try {
        // 调用后端接口（确保地址正确）
        const response = await this.$axios.get('http://localhost:8080/api/projects/');
        const data = response.data || {};

        // 兼容后端两种返回格式：分页对象（含results）/纯数组
        const projectList = Array.isArray(data.results)
          ? data.results
          : (Array.isArray(data) ? data : []);

        // 格式化数据（字段映射+时间格式化）
        this.projects = projectList.map(project => ({
          id: project.id,
          name: project.name || '未命名项目',
          testType: project.test_type || 'apiTest', // 默认值兜底
          testTypeLabel: project.test_type === 'apiTest' ? '接口测试' : 'UI测试',
          // 优化时间格式（避免时区问题）
          createTime: new Date(project.create_time).toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          })
        }));

        // 若有项目，滚动容器自动滚动到最左侧
        this.$nextTick(() => {
          const scrollContainer = document.querySelector('.project-scroll-container');
          if (scrollContainer) scrollContainer.scrollLeft = 0;
        });

      } catch (error) {
        // 错误分类处理：网络错误/接口错误
        const errorMsg = error.message.includes('Network Error')
          ? '网络错误，请检查后端服务是否启动'
          : `加载项目失败：${error.response?.data?.detail || error.message}`;

        this.showModal(errorMsg, 'fail');
        console.error('加载项目失败：', error);
        this.projects = []; // 出错时置空列表，避免页面异常
      }
    },

    /**
     * 卡片点击：跳转到对应测试页面，增加状态管理
     */
    handleCardClick(project) {
      if (this.isNavigating || this.isDeleting) return;

      this.isNavigating = true;
      try {
        // 根据测试类型跳转不同页面，传递完整项目信息
        const routeConfig = {
          apiTest: { path: '/ApiInfo', title: '接口测试' },
          uiTest: { path: '/UiInfo', title: 'UI测试' }
        };

        const config = routeConfig[project.testType];
        if (config) {
          this.$router.push({
            path: config.path,
            query: {
              projectId: project.id,
              projectName: project.name,
              projectType: project.testType
            }
          });
        } else {
          this.showModal(`当前「${project.testTypeLabel}」类型暂不支持查看详情`, 'fail');
          this.isNavigating = false;
        }
      } catch (error) {
        this.showModal('页面跳转失败，请重试', 'fail');
        console.error('跳转失败：', error);
        this.isNavigating = false;
      }
    },

    /**
     * 新增项目：跳转页面，增加加载状态
     */
    handleAddItem() {
      if (this.isNavigating) return;
      this.isNavigating = true;
      this.$router.push('/NewOption').catch(error => {
        this.showModal('跳转新增页面失败，请重试', 'fail');
        console.error('跳转失败：', error);
        this.isNavigating = false;
      });
    },

    /**
     * 触发删除：直接传递项目ID和名称，减少find操作
     */
    handleDeleteProject(projectId, projectName) {
      if (this.isDeleting) return;
      this.deleteProjectId = projectId;
      this.projectName = projectName;
      this.modalType = 'confirm';
      this.modalMessage = `确定要删除项目「${projectName}」吗？\n删除后数据不可恢复！`;
      this.modalVisible = true;
    },

    /**
     * 模态框确认：仅处理删除逻辑（统一入口）
     */
    async handleModalConfirm() {
      // 只有确认删除且有项目ID时执行
      if (this.modalType !== 'confirm' || !this.deleteProjectId) {
        this.modalVisible = false;
        return;
      }

      try {
        this.isDeleting = true;
        this.deleteingProjectId = this.deleteProjectId;

        // 调用后端删除接口（关键：同步删除数据库数据，而非仅前端删除）
        await this.$axios.delete(`http://localhost:8080/api/projects/${this.deleteProjectId}/`);

        // 前端同步更新列表（无需重新请求接口，优化性能）
        this.projects = this.projects.filter(p => p.id !== this.deleteProjectId);
        this.showModal(`项目「${this.projectName}」删除成功！`, 'success');
      } catch (error) {
        const errorMsg = error.response?.data?.detail || '删除失败，请重试';
        this.showModal(`删除项目失败：${errorMsg}`, 'fail');
        console.error('删除项目失败：', error);
      } finally {
        // 重置状态
        this.isDeleting = false;
        this.deleteingProjectId = null;
        this.deleteProjectId = null;
        this.projectName = '';
        this.modalVisible = false;
      }
    },

    /**
     * 显示模态框：封装通用方法，减少重复代码
     */
    showModal(message, type = 'fail') {
      this.modalMessage = message;
      this.modalType = type;
      this.modalVisible = true;

      // 成功/失败弹窗3秒后自动关闭
      if (type === 'success' || type === 'fail') {
        this.modalTimer && clearTimeout(this.modalTimer);
        this.modalTimer = setTimeout(() => {
          this.modalVisible = false;
        }, 3000);
      }
    }
  },
}
</script>

<style scoped>
.home-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 背景图片：修复层级，避免遮挡内容 */
.bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.6; /* 降低透明度，提高文字可读性 */
  z-index: 1;
}

.bg-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none; /* 禁止选中图片 */
}

/* 标题样式：优化位置和视觉效果 */
.page-title {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: 2.5rem;
  color: #2c3e50;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
}

/* 中间卡片容器：优化响应式和阴影 */
.center-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  width: 90%;
  max-width: 1200px;
  min-height: 350px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  padding: 24px;
  box-sizing: border-box;
}

.box-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
}

.box-content h3 {
  margin: 0;
  color: #34495e;
  font-size: 1.4rem;
  font-weight: 500;
}

/* 滚动容器：优化padding和最小高度 */
.project-scroll-container {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 12px 0;
  min-height: 140px;
  position: relative;
  box-sizing: border-box;
}

/* 自定义滚动条：适配主流浏览器 */
.project-scroll-container::-webkit-scrollbar {
  height: 8px;
}
.project-scroll-container::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 10px;
}
.project-scroll-container::-webkit-scrollbar-thumb {
  background: #bdc3c7;
  border-radius: 10px;
  transition: background 0.3s;
}
.project-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #95a5a6;
}
.project-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: #bdc3c7 #f5f5f5;
}

/* 项目列表：优化间距和排列 */
.project-list {
  display: flex;
  gap: 20px;
  width: max-content;
  padding: 8px 0;
}

/* 项目卡片：优化视觉层次和交互 */
.project-card {
  width: 280px;
  min-height: 140px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
  cursor: pointer;
  border: 1px solid #f0f0f0;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
  border-color: #e0e0e0;
}

/* 卡片头部：优化文字溢出处理 */
.card-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
}

.project-name {
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

/* 项目类型标签：区分接口/UI测试 */
.project-type {
  font-size: 0.85rem;
  color: #ffffff;
  padding: 4px 12px;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.type-api {
  background-color: #3498db; /* 接口测试：蓝色 */
}

.type-ui {
  background-color: #2ecc71; /* UI测试：绿色 */
}

/* 卡片底部：优化布局 */
.card-footer {
  font-size: 0.8rem;
  color: #7f8c8d;
  position: relative;
  padding: 6px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.project-time {
  text-align: center;
}

/* 删除按钮：优化位置和状态 */
.delete-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 4px 10px;
  transition: background-color 0.2s;
  z-index: 5;
  display: flex;
  align-items: center
}
</style>