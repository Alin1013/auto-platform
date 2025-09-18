<template>
  <div class="home-container">
    <!-- 背景图片容器 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="主页面背景" />
    </div>
    <!-- 标题文字 -->
    <h2 class="page-title">首页</h2>

    <!-- 中间方框容器 -->
    <div class="center-box">
      <div class="box-content">
        <h3>项目区域</h3>
        <!-- 空项目添加按钮 -->
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
  methods: {
    // 处理添加项目的逻辑
    handleAddItem() {
      // 跳转到新增项目部分
      this.$router.push({ name: 'NewOption' });
    }
  }
}
</script>

<style scoped>
/* 容器：作为页面根容器，占满整个视口 */
.home-container {
  position: relative; /* 作为子元素定位的参考 */
  width: 100vw; /* 宽度占满视口 */
  height: 100vh; /* 高度占满视口 */
  overflow: hidden; /* 防止图片溢出 */
}

/* 背景图片：自适应全屏且固定在底部，降低透明度 */
.bg-image {
  position: absolute;
  bottom: 0; /* 固定在页面最底端 */
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.7; /* 透明度设置，0-1之间，值越小越透明 */
}

.bg-image img {
  width: 100%; /* 图片宽度自适应容器 */
  height: 100%; /* 图片高度自适应容器 */
  object-fit: cover; /* 保持图片比例，填满容器（超出部分裁剪） */
}

/* 标题：顶部中央 */
.page-title {
  position: absolute;
  top: 20px; /* 距离顶部20px（可调整） */
  left: 50%;
  transform: translateX(-50%); /* 水平居中 */
  margin: 0; /* 清除默认margin */
  z-index: 10; /* 确保文字在图片上方 */
  font-size: 2rem; /* 调整标题大小 */
  color: #333; /* 标题颜色，确保在透明背景上清晰可见 */
}

/* 中间方框样式 */
.center-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 完全居中 */
  z-index: 10; /* 确保在背景之上 */
  width: 60%; /* 宽度占屏幕的60%，可调整 */
  max-width: 600px; /* 最大宽度限制 */
  min-height: 300px; /* 最小高度 */
  background-color: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 阴影效果 */
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
  margin-bottom: 20px;
  color: #555;
  font-size: 1.5rem;
}

/* 添加项目按钮样式 */
.add-item-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #42b983; /* 绿色背景 */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-item-btn:hover {
  background-color: #359e75; /* hover时加深颜色 */
}

.add-icon {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
