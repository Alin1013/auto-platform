<template>
  <div class="api-info-container">
    <!-- 背景图片 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="接口测试详情背景" />
    </div>

    <!-- 页面标题 -->
    <h1 class="page-title">{{ currentProjectName }} - 接口测试详情</h1>

    <!-- 主内容区：左侧功能栏 + 右侧内容区（Flex横向布局，确保高度一致） -->
    <div class="main-content">
      <aside class="function-sidebar">
        <button class="back-btn" @click="handleGoBack">◀返回</button>
        <ul class="function-list">
          <li
            class="function-item"
            v-for="item in functionItems"
            :key="item.id"
            @click="activeSection = item.id"
            :class="{ 'active': activeSection === item.id }"
          >
            {{ item.name }}
          </li>
        </ul>
      </aside>

      <!-- 右侧内容区：与左侧高度强制一致，内容溢出滚动 -->
      <main class="content-area">
        <section class="content-section">
          <h2 class="section-title">{{ activeFunctionItem.name }}</h2>
          <div class="section-placeholder">
            <p>当前「{{ activeFunctionItem.name }}」功能区暂未开放，敬请期待...</p>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiInfo',
  props: {
    currentProjectName: {
      type: String,
      required: true,
      default: '未命名接口测试项目'
    }
  },
  data() {
    return {
      functionItems: [
        { id: 'interface-list', name: '接口列表' },
        { id: 'test-case', name: '测试用例' },
        { id: 'test-report', name: '测试报告' },
        { id: 'environment', name: '环境配置' },
        { id: 'log', name: '执行日志' }
      ],
      activeSection: 'interface-list' // 默认激活接口列表
    }
  },
  methods: {
    // 返回首页
    handleGoBack() {
      this.$router.push('/home');
    }
  },
  computed: {
    // 直接获取激活项
    activeFunctionItem() {
      return this.functionItems.find(item => item.id === this.activeSection) || { name: '未知功能' };
    }
  }
}
</script>

<style scoped>
/* 根容器：基础布局*/
.api-info-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  padding: 80px 20px 20px; /* 上下内边距，左右留空适配小屏幕 */
  box-sizing: border-box;
}

/* 背景图片：全屏覆盖，不影响内容布局 */
.bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.7;
  z-index: -1;
}
.bg-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 页面标题：自适应居中，避免遮挡 */
.page-title {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: clamp(1.5rem, 3vw, 2rem); /* 响应式字体大小 */
  color: #333;
  font-weight: 600;
  white-space: nowrap; /* 防止标题换行 */
}

/* 确保左右区域高度一致 */
.main-content {
  display: flex;
  gap: 24px; /* 左右区域间距 */
  width: 100%;
  height: 100%; /* 占满根容器剩余高度 */
  min-height: 300px; /* 最小高度，避免内容过短时布局坍塌 */
}

.function-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px; /* 返回按钮与列表间距 */
  width: clamp(160px, 20vw, 200px); /* 响应式宽度 */
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  box-sizing: border-box;
}

/* 返回按钮 */
.back-btn {
  background: transparent;
  border: none;
  color: #333;
  font-size: 1rem;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.3s;
  text-align: left;
}
.back-btn:hover {
  background-color: #f5f5f5;
  color: #2196F3;
}

/* 功能列表 */
.function-list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}
.function-item {
  padding: 12px 16px;
  color: #555;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 4px;
  margin-bottom: 4px;
}
.function-item.active {
  background-color: #2196F3; /* 接口测试主题色：蓝色 */
  color: white;
  font-weight: 500;
}
.function-item:not(.active):hover {
  background-color: #f5f5f5;
  color: #2196F3;
}

.content-area {
  flex: 1;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 32px;
  box-sizing: border-box;
  overflow-y: auto;
}

/* 右侧内容区内部样式 */
.content-section {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.section-title {
  color: #333;
  font-size: 1.5rem;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}
.section-placeholder {
  color: #888;
  font-size: 1rem;
  line-height: 1.6;
  padding: 48px 0;
  text-align: center;
  background-color: #fafafa;
  border-radius: 4px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 滚动条样式 */
.content-area::-webkit-scrollbar,
.function-sidebar::-webkit-scrollbar {
  width: 6px;
}
.content-area::-webkit-scrollbar-track,
.function-sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
.content-area::-webkit-scrollbar-thumb,
.function-sidebar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}
.content-area::-webkit-scrollbar-thumb:hover,
.function-sidebar::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .api-info-container {
    padding: 70px 10px 10px;
  }
  .page-title {
    font-size: 1.2rem;
  }
  .main-content {
    gap: 12px;
  }
  .function-sidebar {
    padding: 12px;
  }
  .content-area {
    padding: 16px;
  }
}
</style>
