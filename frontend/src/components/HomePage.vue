<template>
  <div class="home-container">
    <!-- 个人中心入口 -->
    <div class="user-profile" @click="handleProfileClick">
      <img :src="userAvatar" alt="用户头像" class="avatar" />
    </div>

    <!-- 背景图片容器 -->
    <div class="bg-image">
      <img :src="backgroundImg" alt="主页面背景" />
    </div>

    <!-- 标题文字 -->
    <h1 class="page-title">项目</h1>

    <!-- 中间方框容器 -->
    <div class="center-box">
      <div class="box-content">
        <h3>项目区域</h3>

        <!-- 横向滑动容器 -->
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
                <span
                  class="project-type"
                  :class="project.testType === 'apiTest' ? 'type-api' : 'type-ui'"
                >
                  {{ project.testTypeLabel }}
                </span>
              </div>
              <div class="card-footer">
                <span class="project-time">{{ project.createTime }}</span>
                <button
                  class="delete-btn"
                  @click.stop="handleDeleteProject(project.id, project.name)"
                  :disabled="isDeleting || deleteingProjectId === project.id"
                >
                  {{ isDeleting && deleteingProjectId === project.id ? '删除中...' : '删除' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 无项目提示 -->
          <div class="no-project" v-else>
            <i class="no-project-icon">📂</i>
            <p>暂无项目</p>
            <p class="no-project-tip">点击下方「添加新项目」开始</p>
          </div>
        </div>

        <!-- 添加新项目按钮 -->
        <button
          class="add-item-btn"
          @click="handleAddItem"
          :disabled="isNavigating || isDeleting"
        >
          <i class="add-icon">+</i>
          <span>{{ isNavigating ? '跳转中...' : '添加新项目' }}</span>
        </button>
      </div>
    </div>

    <!-- 统一模态框 -->
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
import backgroundImg from '@/assets/background.png';
import FailModal from '@/components/FailModal.vue';
import request from "@/utils/request";
import { mapState } from 'vuex'; // 导入Vuex辅助函数

export default {
  name: 'HomePage',
  components: { FailModal },
  data() {
    return {
      backgroundImg,
      projects: [],
      modalVisible: false,
      modalMessage: '',
      modalType: 'fail',
      deleteProjectId: null,
      deleteingProjectId: null,
      projectName: '',
      isDeleting: false,
      isNavigating: false,
      modalTimer: null
    }
  },
  computed: {
    // 从Vuex获取用户头像
    ...mapState({
      userInfo: state => state.userInfo
    }),
    // 计算用户头像地址，优先使用用户信息中的头像，否则使用默认头像
    userAvatar() {
      return this.userInfo.avatarUrl 
        ? this.userInfo.avatarUrl 
        : require('@/assets/user-avatar.png');
    }
  },
  mounted() {
    this.loadProjects();
    // 页面加载时获取用户信息
    this.fetchUserInfo();
  },
  watch: {
    $route: {
      handler: 'loadProjects',
      immediate: false,
      deep: false
    }
  },
  methods: {
    // 获取当前登录用户信息
    async fetchUserInfo() {
      try {
        const response = await request.get('/user/me/');
        this.$store.commit('SET_USER_INFO', {
          username: response.data.username,
          avatarUrl: response.data.avatar
        });
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 失败时不影响主流程，继续使用默认头像
      }
    },

    handleProfileClick() {
      if (this.isNavigating || this.isDeleting) return;

      this.isNavigating = true;
      this.$router.push('/UserProfile')
        .then(() => {
          this.isNavigating = false;
        })
        .catch(error => {
          this.showModal('跳转到个人中心失败，请重试', 'fail');
          console.error('个人中心跳转失败：', error);
          this.isNavigating = false;
        });
    },

    async loadProjects() {
      try {
        const response = await request.get('/api/core/projects/');
        const data = response.data || {};

        const projectList = Array.isArray(data.results)
          ? data.results
          : (Array.isArray(data) ? data : []);

        this.projects = projectList.map(project => ({
          id: project.id,
          name: project.name || '未命名项目',
          testType: project.test_type || 'apiTest',
          testTypeLabel: project.test_type === 'apiTest' ? '接口测试' : 'UI测试',
          createTime: project.create_time
            ? new Date(project.create_time).toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
              })
            : '未知时间'
        }));

        this.$nextTick(() => {
          const scrollContainer = document.querySelector('.project-scroll-container');
          if (scrollContainer) scrollContainer.scrollLeft = 0;
        });

      } catch (error) {
        let errorMsg;
        if (error.message.includes('Network Error')) {
          errorMsg = '网络错误，请检查后端服务是否启动';
        } else if (error.response) {
          errorMsg = `加载失败：${error.response.data?.detail || '服务器内部错误'}`;
        } else {
          errorMsg = `加载失败：${error.message}`;
        }

        this.showModal(errorMsg, 'fail');
        console.error('加载项目列表错误：', error);
        this.projects = [];
      }
    },

    handleCardClick(project) {
      if (this.isNavigating || this.isDeleting) return;

      this.isNavigating = true;
      const routeMap = {
        apiTest: '/ApiInfo',
        uiTest: '/UiInfo'
      };

      const targetRoute = routeMap[project.testType];
      if (targetRoute) {
        this.$router.push({
          path: targetRoute,
          query: {
            projectId: project.id,
            projectName: project.name,
            projectType: project.testType
          }
        })
        .then(() => {
          this.isNavigating = false;
        })
        .catch(error => {
          this.showModal('跳转项目详情失败，请重试', 'fail');
          console.error('项目跳转错误：', error);
          this.isNavigating = false;
        });
      } else {
        this.showModal(`当前「${project.testTypeLabel}」类型暂不支持查看`, 'fail');
        this.isNavigating = false;
      }
    },

    handleAddItem() {
      if (this.isNavigating || this.isDeleting) return;

      this.isNavigating = true;
      this.$router.push('/NewOption')
        .then(() => {
          this.isNavigating = false;
        })
        .catch(error => {
          this.showModal('跳转新增项目页面失败，请重试', 'fail');
          console.error('新增项目跳转错误：', error);
          this.isNavigating = false;
        });
    },

    handleDeleteProject(projectId, projectName) {
      if (this.isDeleting) return;

      this.deleteProjectId = projectId;
      this.projectName = projectName;
      this.modalType = 'confirm';
      this.modalMessage = `确定要删除项目「${projectName}」吗？\n删除后数据不可恢复！`;
      this.modalVisible = true;
    },

    async handleModalConfirm() {
      if (this.modalType !== 'confirm' || !this.deleteProjectId) {
        this.modalVisible = false;
        return;
      }

      try {
        this.isDeleting = true;
        this.deleteingProjectId = this.deleteProjectId;

        await request.delete(`/api/projects/${this.deleteProjectId}/`);

        this.projects = this.projects.filter(p => p.id !== this.deleteProjectId);
        this.showModal(`项目「${this.projectName}」删除成功！`, 'success');
      } catch (error) {
        const errorMsg = error.response?.data?.detail || '服务器删除接口异常';
        this.showModal(`删除失败：${errorMsg}`, 'fail');
        console.error('删除项目错误：', error);
      } finally {
        this.isDeleting = false;
        this.deleteingProjectId = null;
        this.deleteProjectId = null;
        this.projectName = null;
        this.modalVisible = false;
      }
    },

    showModal(message, type = 'fail') {
      if (this.modalTimer) {
        clearTimeout(this.modalTimer);
        this.modalTimer = null;
      }

      this.modalMessage = message;
      this.modalType = type;
      this.modalVisible = true;

      if (type === 'success' || type === 'fail') {
        this.modalTimer = setTimeout(() => {
          this.modalVisible = false;
          this.modalTimer = null;
        }, 3000);
      }
    }
  },
  beforeUnmount() {
    if (this.modalTimer) {
      clearTimeout(this.modalTimer);
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.6;
  z-index: 1;
}

.bg-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
}

.page-title {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: clamp(1.8rem, 5vw, 2.5rem);
  color: #2c3e50;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
}

.center-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  width: 90%;
  max-width: 1200px;
  min-height: 350px;
  max-height: 80vh;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
}

.box-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.box-content h3 {
  margin: 0;
  color: #34495e;
  font-size: 1.4rem;
  font-weight: 500;
}

.project-scroll-container {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 12px 0;
  min-height: 140px;
  box-sizing: border-box;
}

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

.project-list {
  display: flex;
  gap: 20px;
  width: max-content;
  padding: 8px 0;
}

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
  cursor: pointer;
  border: 1px solid #f0f0f0;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
  border-color: #e0e0e0;
}

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

.project-type {
  font-size: 0.85rem;
  color: #ffffff;
  padding: 4px 12px;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.type-api {
  background-color: #3498db;
}

.type-ui {
  background-color: #2ecc71;
}

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
  align-items: center;
}

.user-profile {
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 20;
  cursor: pointer;
  transition: transform 0.3s;
}

.user-profile:hover {
  transform: scale(1.05);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-item-btn {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.add-item-btn:hover {
  background-color: #2980b9;
}

.add-item-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.add-icon {
  font-size: 1.2rem;
}

.no-project {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #7f8c8d;
}

.no-project-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.no-project-tip {
  font-size: 0.9rem;
  margin-top: 5px;
  color: #95a5a6;
}
</style>