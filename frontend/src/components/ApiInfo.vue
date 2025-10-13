<template>
  <div class="api-info-container">
    <!-- 背景图片 -->
    <div class="bg-image">
      <img src="@/assets/background.png" alt="接口测试详情背景"/>
    </div>

    <!-- 页面标题 -->
    <h1 class="page-title">{{ currentProjectName }} - 接口测试详情</h1>

    <!-- 主内容区：左侧功能栏 + 右侧内容区 -->
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

      <!-- 右侧内容区 -->
      <main class="content-area">
        <section class="content-section">
          <h2 class="section-title">{{ activeFunctionItem.name }}</h2>

          <!-- 接口列表内容（Postman风格） -->
          <div v-if="activeSection === 'interface-list'" class="interface-list-content">
            <!-- 接口信息卡片 -->
            <div class="interface-card">
              <!-- 请求URL和方法 -->
              <div class="request-header">
                <div class="method-selector">
                  <select v-model="selectedMethod" class="method-dropdown">
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="PATCH">PATCH</option>
                    <option value="HEAD">HEAD</option>
                    <option value="OPTIONS">OPTIONS</option>
                  </select>
                </div>
                <div class="url-input-group">
                  <input
                      type="text"
                      v-model="host"
                      class="host-input"
                      placeholder="Host"
                  >
                  <span class="url-separator">/</span>
                  <input
                      type="text"
                      v-model="endpoint"
                      class="endpoint-input"
                      placeholder="接口路径"
                  >
                </div>
                <button class="send-btn" @click="sendRequest">
                  <i class="send-icon">▶</i> 发送
                </button>
              </div>

              <!-- 请求标签页 -->
              <div class="request-tabs">
                <div
                    class="tab-item"
                    :class="{ 'active': activeTab === 'params' }"
                    @click="activeTab = 'params'"
                >
                  参数
                </div>
                <div
                    class="tab-item"
                    :class="{ 'active': activeTab === 'headers' }"
                    @click="activeTab = 'headers'"
                >
                  请求头
                </div>
                <div
                    class="tab-item"
                    :class="{ 'active': activeTab === 'body' }"
                    @click="activeTab = 'body'"
                >
                  请求体
                </div>
                <div
                    class="tab-item"
                    :class="{ 'active': activeTab === 'auth' }"
                    @click="activeTab = 'auth'"
                >
                  认证
                </div>
              </div>

              <!-- 请求参数内容 -->
              <div class="tab-content">
                <!-- 参数表单 -->
                <div v-if="activeTab === 'params'" class="params-content">
                  <div class="params-table">
                    <div class="params-header">
                      <div class="param-column">参数名</div>
                      <div class="param-column">值</div>
                      <div class="param-column">描述</div>
                      <div class="param-column">操作</div>
                    </div>
                    <div v-for="(param, index) in params" :key="index" class="param-row">
                      <input
                          type="text"
                          v-model="param.key"
                          class="param-input"
                          placeholder="参数名"
                      >
                      <input
                          type="text"
                          v-model="param.value"
                          class="param-input"
                          placeholder="值"
                      >
                      <input
                          type="text"
                          v-model="param.description"
                          class="param-input"
                          placeholder="描述"
                      >
                      <button
                          class="remove-btn"
                          @click="removeParam(index)"
                          :disabled="params.length <= 1"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                  <button class="add-btn" @click="addParam">
                    + 添加参数
                  </button>
                </div>

                <!-- 请求头内容 -->
                <div v-if="activeTab === 'headers'" class="headers-content">
                  <div class="headers-table">
                    <div class="header-header">
                      <div class="header-column">Key</div>
                      <div class="header-column">Value</div>
                      <div class="header-column">操作</div>
                    </div>
                    <div v-for="(header, index) in headers" :key="index" class="header-row">
                      <input
                          type="text"
                          v-model="header.key"
                          class="header-input"
                          placeholder="Key"
                      >
                      <input
                          type="text"
                          v-model="header.value"
                          class="header-input"
                          placeholder="Value"
                      >
                      <button
                          class="remove-btn"
                          @click="removeHeader(index)"
                          :disabled="headers.length <= 1"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                  <button class="add-btn" @click="addHeader">
                    + 添加请求头
                  </button>
                </div>

                <!-- 请求体内容 -->
                <div v-if="activeTab === 'body'" class="body-content">
                  <div class="body-type-selector">
                    <div
                        class="body-type-item"
                        :class="{ 'active': bodyType === 'form-data' }"
                        @click="bodyType = 'form-data'"
                    >
                      form-data
                    </div>
                    <div
                        class="body-type-item"
                        :class="{ 'active': bodyType === 'x-www-form-urlencoded' }"
                        @click="bodyType = 'x-www-form-urlencoded'"
                    >
                      x-www-form-urlencoded
                    </div>
                    <div
                        class="body-type-item"
                        :class="{ 'active': bodyType === 'raw' }"
                        @click="bodyType = 'raw'"
                    >
                      raw
                    </div>
                    <div
                        class="body-type-item"
                        :class="{ 'active': bodyType === 'binary' }"
                        @click="bodyType = 'binary'"
                    >
                      binary
                    </div>
                  </div>

                  <!-- raw类型的内容 -->
                  <div v-if="bodyType === 'raw'" class="raw-body-content">
                    <select v-model="rawBodyType" class="raw-type-selector">
                      <option value="json">JSON</option>
                      <option value="xml">XML</option>
                      <option value="text">Text</option>
                      <option value="javascript">JavaScript</option>
                      <option value="html">HTML</option>
                      <option value="css">CSS</option>
                    </select>
                    <textarea
                        v-model="rawBodyContent"
                        class="raw-body-input"
                        placeholder="输入请求体内容..."
                    ></textarea>
                  </div>

                  <!-- form-data类型的内容 -->
                  <div v-if="bodyType === 'form-data'" class="form-data-content">
                    <div class="form-data-table">
                      <div class="form-data-header">
                        <div class="form-data-column">Key</div>
                        <div class="form-data-column">Value</div>
                        <div class="form-data-column">类型</div>
                        <div class="form-data-column">操作</div>
                      </div>
                      <div v-for="(field, index) in formDataFields" :key="index" class="form-data-row">
                        <input
                            type="text"
                            v-model="field.key"
                            class="form-data-input"
                            placeholder="Key"
                        >
                        <input
                            type="text"
                            v-model="field.value"
                            class="form-data-input"
                            placeholder="Value"
                            v-if="field.type === 'text'"
                        >
                        <input
                            type="file"
                            class="form-data-file"
                            v-if="field.type === 'file'"
                        >
                        <select
                            v-model="field.type"
                            class="form-data-type"
                            @change="updateFormFieldType(index, field.type)"
                        >
                          <option value="text">text</option>
                          <option value="file">file</option>
                        </select>
                        <button
                            class="remove-btn"
                            @click="removeFormDataField(index)"
                            :disabled="formDataFields.length <= 1"
                        >
                          ×
                        </button>
                      </div>
                    </div>
                    <button class="add-btn" @click="addFormDataField">
                      + 添加字段
                    </button>
                  </div>

                  <!-- 其他类型的占位符 -->
                  <div v-if="['x-www-form-urlencoded', 'binary'].includes(bodyType)" class="body-placeholder">
                    <p>{{ bodyType }} 类型的请求体功能即将支持</p>
                  </div>
                </div>

                <!-- 认证内容 -->
                <div v-if="activeTab === 'auth'" class="auth-content">
                  <div class="auth-type-selector">
                    <select v-model="authType" class="auth-type-dropdown">
                      <option value="none">无</option>
                      <option value="basic">Basic Auth</option>
                      <option value="bearer">Bearer Token</option>
                      <option value="digest">Digest Auth</option>
                      <option value="oauth1">OAuth 1.0</option>
                      <option value="oauth2">OAuth 2.0</option>
                    </select>
                  </div>

                  <!-- Basic Auth -->
                  <div v-if="authType === 'basic'" class="auth-fields">
                    <div class="auth-field">
                      <label>用户名</label>
                      <input type="text" v-model="authData.username" class="auth-input">
                    </div>
                    <div class="auth-field">
                      <label>密码</label>
                      <input type="password" v-model="authData.password" class="auth-input">
                    </div>
                  </div>

                  <!-- Bearer Token -->
                  <div v-if="authType === 'bearer'" class="auth-fields">
                    <div class="auth-field">
                      <label>Token</label>
                      <input type="text" v-model="authData.token" class="auth-input">
                    </div>
                  </div>

                  <!-- 其他认证类型占位符 -->
                  <div v-if="['digest', 'oauth1', 'oauth2'].includes(authType)" class="auth-placeholder">
                    <p>{{ authType }} 认证类型即将支持</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 响应区域 -->
            <div class="response-section">
              <div class="response-header">
                <div class="response-status" v-if="responseData">
                  <span class="status-code" :class="statusCodeClass">{{ responseData.status }}</span>
                  <span class="response-time">{{ responseTime }}ms</span>
                  <span class="response-size">{{ responseSize }}B</span>
                </div>
                <div class="response-tabs">
                  <div
                      class="response-tab-item"
                      :class="{ 'active': activeResponseTab === 'body' }"
                      @click="activeResponseTab = 'body'"
                  >
                    响应体
                  </div>
                  <div
                      class="response-tab-item"
                      :class="{ 'active': activeResponseTab === 'headers' }"
                      @click="activeResponseTab = 'headers'"
                  >
                    响应头
                  </div>
                  <div
                      class="response-tab-item"
                      :class="{ 'active': activeResponseTab === 'cookies' }"
                      @click="activeResponseTab = 'cookies'"
                  >
                    Cookies
                  </div>
                  <div
                      class="response-tab-item"
                      :class="{ 'active': activeResponseTab === 'timeline' }"
                      @click="activeResponseTab = 'timeline'"
                  >
                    时间线
                  </div>
                </div>
                <div class="response-actions">
                  <button class="response-action-btn" @click="copyResponse">
                    复制
                  </button>
                  <button class="response-action-btn" @click="saveResponse">
                    保存
                  </button>
                  <select v-model="responseViewFormat" class="response-view-select">
                    <option value="pretty">美化</option>
                    <option value="raw">原始</option>
                    <option value="preview">预览</option>
                  </select>
                </div>
              </div>

              <!-- 响应内容 -->
              <div class="response-content">
                <div v-if="activeResponseTab === 'body'">
                  <pre v-if="responseData" class="response-body">{{ formatResponseData() }}</pre>
                  <div v-else-if="responseError" class="error-message">{{ responseError }}</div>
                  <div v-else class="empty-response">
                    <p>发送请求后将显示响应结果</p>
                  </div>
                </div>

                <div v-if="activeResponseTab === 'headers'" class="response-headers">
                  <div v-if="responseData && responseData.headers" class="headers-list">
                    <div v-for="(value, key) in responseData.headers" :key="key" class="header-item">
                      <span class="header-key">{{ key }}:</span>
                      <span class="header-value">{{ value }}</span>
                    </div>
                  </div>
                  <div v-else class="empty-section">
                    <p>无响应头数据</p>
                  </div>
                </div>

                <div v-if="activeResponseTab === 'cookies'" class="response-cookies">
                  <div v-if="responseData && responseData.cookies && responseData.cookies.length > 0"
                       class="cookies-list">
                    <div v-for="(cookie, index) in responseData.cookies" :key="index" class="cookie-item">
                      <span class="cookie-name">{{ cookie.name }}:</span>
                      <span class="cookie-value">{{ cookie.value }}</span>
                    </div>
                  </div>
                  <div v-else class="empty-section">
                    <p>无Cookies数据</p>
                  </div>
                </div>

                <div v-if="activeResponseTab === 'timeline'" class="response-timeline">
                  <div v-if="responseData" class="timeline-chart">
                    <div class="timeline-bar">
                      <div class="timeline-segment dns" :style="{ width: timelineData.dns + '%' }"
                           title="DNS: {{ timelineData.dnsMs }}ms"></div>
                      <div class="timeline-segment connect" :style="{ width: timelineData.connect + '%' }"
                           title="连接: {{ timelineData.connectMs }}ms"></div>
                      <div class="timeline-segment send" :style="{ width: timelineData.send + '%' }"
                           title="发送: {{ timelineData.sendMs }}ms"></div>
                      <div class="timeline-segment wait" :style="{ width: timelineData.wait + '%' }"
                           title="等待: {{ timelineData.waitMs }}ms"></div>
                      <div class="timeline-segment receive" :style="{ width: timelineData.receive + '%' }"
                           title="接收: {{ timelineData.receiveMs }}ms"></div>
                    </div>
                    <div class="timeline-stats">
                      <div class="timeline-stat">
                        <span class="stat-label">DNS:</span>
                        <span class="stat-value">{{ timelineData.dnsMs }}ms</span>
                      </div>
                      <div class="timeline-stat">
                        <span class="stat-label">连接:</span>
                        <span class="stat-value">{{ timelineData.connectMs }}ms</span>
                      </div>
                      <div class="timeline-stat">
                        <span class="stat-label">发送:</span>
                        <span class="stat-value">{{ timelineData.sendMs }}ms</span>
                      </div>
                      <div class="timeline-stat">
                        <span class="stat-label">等待:</span>
                        <span class="stat-value">{{ timelineData.waitMs }}ms</span>
                      </div>
                      <div class="timeline-stat">
                        <span class="stat-label">接收:</span>
                        <span class="stat-value">{{ timelineData.receiveMs }}ms</span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="empty-section">
                    <p>无时间线数据</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 测试用例内容 -->
          <div v-if="activeSection === 'test-case'" class="test-case-content">
            <div class="test-case-actions">
              <button class="add-btn" @click="showAddTestCaseModal = true">
                + 添加测试用例
              </button>
            </div>

            <div v-if="testCases.length > 0" class="test-case-list">
              <div v-for="(testCase, index) in testCases" :key="index" class="test-case-card">
                <div class="test-case-header">
                  <h3 class="test-case-title">{{ testCase.name }}</h3>
                  <button class="remove-btn" @click="handleDeleteTestCase(index, testCase.name)">×</button>
                </div>
                <div class="test-case-body">
                  <p><strong>URL:</strong> {{ testCase.url }}</p>
                  <p><strong>方法:</strong> {{ testCase.method }}</p>
                  <p v-if="testCase.description"><strong>描述:</strong> {{ testCase.description }}</p>
                </div>
              </div>
            </div>

            <div v-else class="empty-test-case">
              <p>暂无测试用例，请点击"添加测试用例"按钮创建</p>
            </div>
          </div>

          <!-- 添加测试用例弹窗 -->
          <div v-if="showAddTestCaseModal" class="modal-overlay">
            <div class="modal-container">
              <div class="modal-header">
                <h3>添加测试用例</h3>
                <button class="modal-close" @click="showAddTestCaseModal = false">×</button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="handleAddTestCase">
                  <div class="form-item">
                    <label class="form-label">用例名称</label>
                    <input
                        type="text"
                        v-model="newTestCase.name"
                        class="form-control"
                        placeholder="请输入测试用例名称"
                        required
                    >
                  </div>
                  <div class="form-item">
                    <label class="form-label">请求URL</label>
                    <input
                        type="text"
                        v-model="newTestCase.url"
                        class="form-control"
                        placeholder="请输入请求URL"
                        required
                    >
                  </div>
                  <div class="form-item">
                    <label class="form-label">请求方法</label>
                    <select v-model="newTestCase.method" class="form-control" required>
                      <option value="GET">GET</option>
                      <option value="POST">POST</option>
                      <option value="PUT">PUT</option>
                      <option value="DELETE">DELETE</option>
                    </select>
                  </div>
                  <div class="form-item">
                    <label class="form-label">用例描述</label>
                    <textarea
                        v-model="newTestCase.description"
                        class="form-control"
                        placeholder="请输入测试用例描述"
                        rows="3"
                    ></textarea>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="cancel-btn" @click="showAddTestCaseModal = false">取消</button>
                    <button type="submit" class="confirm-btn">确定</button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <!-- 其他功能区占位符 -->
          <div v-else-if="['test-report', 'environment', 'log'].includes(activeSection)" class="section-placeholder">
            <p>当前「{{ activeFunctionItem.name }}」功能区暂未开放，敬请期待...</p>
          </div>
        </section>
      </main>
    </div>

    <!-- 成功提示弹窗 -->
    <SuccessModal
      v-if="showSuccessModal"
      :project-name="successMessage"
      :on-confirm="handleSuccessConfirm"
    />

    <!-- 失败/确认提示弹窗 -->
    <FailModal
      :visible="showFailModal"
      :message="failMessage"
      :type="failModalType"
      @close="showFailModal = false"
      @confirm="handleFailConfirm"
    />
  </div>
</template>

<script>
import request from '@/utils/request';
import axios from "axios";

export default {
  data() {
    return {
      currentProjectName: '',
      testCases: [],
      selectedTestCase: null,
      // 表单数据
      formData: {
        name: '',
        url: '',
        method: 'GET',
        headers: '',
        params: '',
        body: ''
      },
      // 功能项配置（与UiInfo保持一致结构）
      functionItems: [
        { id: 'interface-list', name: '接口列表' },
        { id: 'test-case', name: '测试用例' },
        { id: 'test-report', name: '测试报告' },
        { id: 'environment', name: '环境配置' },
        { id: 'log', name: '日志' }
      ],
      activeSection: 'interface-list', // 默认激活接口列表
      // 其他必要数据
      selectedMethod: 'GET',
      host: '',
      endpoint: '',
      activeTab: 'params',
      params: [{ key: '', value: '', description: '' }],
      headers: [{ key: '', value: '' }],
      bodyType: 'form-data',
      rawBodyType: 'json',
      rawBodyContent: '',
      formDataFields: [{ key: '', value: '', type: 'text' }],
      authType: 'none',
      authData: {
        username: '',
        password: '',
        token: ''
      },
      responseData: null,
      responseError: null,
      responseTime: 0,
      responseSize: 0,
      activeResponseTab: 'body',
      responseViewFormat: 'pretty',
      timelineData: {
        dns: 0,
        connect: 0,
        send: 0,
        wait: 0,
        receive: 0,
        dnsMs: 0,
        connectMs: 0,
        sendMs: 0,
        waitMs: 0,
        receiveMs: 0
      },
      showAddTestCaseModal: false,
      newTestCase: {
        name: '',
        url: '',
        method: 'GET',
        description: ''
      },
      showSuccessModal: false,
      successMessage: '',
      showFailModal: false,
      failMessage: '',
      failModalType: 'confirm'
    };
  },
  computed: {
    // 获取激活的功能项
    activeFunctionItem() {
      return this.functionItems.find(item => item.id === this.activeSection) || { name: '未知功能' };
    },
    // 状态码样式
    statusCodeClass() {
      if (!this.responseData) return '';
      const status = this.responseData.status;
      if (status >= 200 && status < 300) return 'success';
      if (status >= 300 && status < 400) return 'redirect';
      if (status >= 400 && status < 500) return 'client-error';
      if (status >= 500) return 'server-error';
      return '';
    }
  },
  mounted() {
    // 从路由参数获取项目名称
    this.currentProjectName = this.$route.query.projectName || '';
    this.loadTestCases();
  },
  methods: {
    // 返回首页
    handleGoBack() {
      this.$router.push('/home');
    },
    // 获取项目下的接口用例
    async loadTestCases() {
      try {
        const projectRes = await request.get(`/api/core/projects/?name=${this.currentProjectName}`);
        if (!projectRes.data.results || projectRes.data.results.length === 0) {
          this.$message.error('未找到对应项目');
          return;
        }
        const projectId = projectRes.data.results[0].id;

        const res = await request.get(`/api/api-test/test-cases/?project=${projectId}`);
        this.testCases = res.data.results;
      } catch (err) {
        console.error('加载用例失败', err);
        this.$message.error('加载用例失败，请重试');
      }
    },
    // 保存接口用例
    async saveTestCase() {
      try {
        const projectRes = await request.get(`/api/core/projects/?name=${this.currentProjectName}`);
        if (!projectRes.data.results || projectRes.data.results.length === 0) {
          this.$message.error('未找到对应项目');
          return;
        }
        const projectId = projectRes.data.results[0].id;

        await request.post('/api/api-test/test-cases/', {
          ...this.formData,
          project: projectId
        });
        this.$message.success('保存成功');
        this.loadTestCases();
      } catch (err) {
        console.error('保存失败', err);
        this.$message.error('保存失败，请重试');
      }
    },
    // 发送接口请求
    async sendRequest() {
      try {
        // 组合完整URL
        const fullUrl = this.host + (this.endpoint ? '/' + this.endpoint : '');
        if (!fullUrl) {
          this.$message.error('请输入完整URL');
          return;
        }

        // 收集请求参数
        const requestData = {
          method: this.selectedMethod,
          url: fullUrl,
          headers: this.headers.reduce((obj, item) => {
            if (item.key) obj[item.key] = item.value;
            return obj;
          }, {}),
          params: this.params.reduce((obj, item) => {
            if (item.key) obj[item.key] = item.value;
            return obj;
          }, {})
        };

        // 添加请求体
        if (this.bodyType === 'raw' && this.rawBodyContent) {
          try {
            requestData.data = this.rawBodyType === 'json'
              ? JSON.parse(this.rawBodyContent)
              : this.rawBodyContent;
          } catch (e) {
            this.$message.error('请求体格式错误');
            return;
          }
        } else if (this.bodyType === 'form-data') {
          const formData = new FormData();
          this.formDataFields.forEach(field => {
            if (field.key) formData.append(field.key, field.value);
          });
          requestData.data = formData;
        }

        // 添加认证信息
        if (this.authType === 'basic' && this.authData.username && this.authData.password) {
          requestData.auth = {
            username: this.authData.username,
            password: this.authData.password
          };
        } else if (this.authType === 'bearer' && this.authData.token) {
          requestData.headers.Authorization = `Bearer ${this.authData.token}`;
        }

        // 记录请求时间
        const startTime = Date.now();
        const response = await axios(requestData);
        const endTime = Date.now();

        // 处理响应数据
        this.responseTime = endTime - startTime;
        this.responseData = response;
        this.responseError = null;

        // 估算响应大小
        this.responseSize = JSON.stringify(response.data).length;

        // 模拟时间线数据（实际项目中应从性能API获取）
        this.timelineData = {
          dns: 10,
          connect: 20,
          send: 15,
          wait: 40,
          receive: 15,
          dnsMs: Math.round(this.responseTime * 0.1),
          connectMs: Math.round(this.responseTime * 0.2),
          sendMs: Math.round(this.responseTime * 0.15),
          waitMs: Math.round(this.responseTime * 0.4),
          receiveMs: Math.round(this.responseTime * 0.15)
        };

      } catch (err) {
        console.error('请求失败', err);
        this.responseError = err.response?.data || err.message;
        this.responseData = err.response || null;
        this.responseTime = 0;
      }
    },
    // 格式化响应数据
    formatResponseData() {
      if (!this.responseData) return '';
      if (this.responseViewFormat === 'raw') {
        return JSON.stringify(this.responseData.data);
      }
      return JSON.stringify(this.responseData.data, null, 2);
    },
    // 复制响应
    copyResponse() {
      if (!this.responseData) return;
      const text = this.formatResponseData();
      navigator.clipboard.writeText(text).then(() => {
        this.$message.success('复制成功');
      }).catch(() => {
        this.$message.error('复制失败');
      });
    },
    // 保存响应（作为测试用例）
    saveResponse() {
      if (!this.responseData) return;
      this.showAddTestCaseModal = true;
      this.newTestCase.url = this.host + (this.endpoint ? '/' + this.endpoint : '');
      this.newTestCase.method = this.selectedMethod;
    },
    // 添加测试用例
    async handleAddTestCase() {
      try {
        const projectRes = await request.get(`/api/core/projects/?name=${this.currentProjectName}`);
        if (!projectRes.data.results || projectRes.data.results.length === 0) {
          this.$message.error('未找到对应项目');
          return;
        }
        const projectId = projectRes.data.results[0].id;

        await request.post('/api/api-test/test-cases/', {
          ...this.newTestCase,
          project: projectId
        });
        this.$message.success('测试用例添加成功');
        this.showAddTestCaseModal = false;
        this.newTestCase = { name: '', url: '', method: 'GET', description: '' };
        this.loadTestCases();
      } catch (err) {
        console.error('添加测试用例失败', err);
        this.$message.error('添加测试用例失败，请重试');
      }
    },
    // 删除测试用例
    async handleDeleteTestCase(index, name) {
      if (confirm(`确定要删除测试用例「${name}」吗？`)) {
        try {
          const testCase = this.testCases[index];
          await request.delete(`/api/api-test/test-cases/${testCase.id}/`);
          this.testCases.splice(index, 1);
          this.$message.success('删除成功');
        } catch (err) {
          console.error('删除失败', err);
          this.$message.error('删除失败，请重试');
        }
      }
    },
    // 参数操作
    addParam() {
      this.params.push({ key: '', value: '', description: '' });
    },
    removeParam(index) {
      this.params.splice(index, 1);
    },
    // 请求头操作
    addHeader() {
      this.headers.push({ key: '', value: '' });
    },
    removeHeader(index) {
      this.headers.splice(index, 1);
    },
    // 表单数据操作
    addFormDataField() {
      this.formDataFields.push({ key: '', value: '', type: 'text' });
    },
    removeFormDataField(index) {
      this.formDataFields.splice(index, 1);
    },
    updateFormFieldType(index, type) {
      this.formDataFields[index].type = type;
    },
    // 弹窗回调
    handleSuccessConfirm() {
      this.showSuccessModal = false;
    },
    handleFailConfirm() {
      this.showFailModal = false;
    }
  }
};
</script>

<style scoped>
/* 根容器样式 */
.api-info-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  padding: 80px 20px 20px;
  box-sizing: border-box;
}

/* 背景图片 */
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

/* 页面标题 */
.page-title {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  z-index: 10;
  font-size: clamp(1.5rem, 3vw, 2rem);
  color: #333;
  font-weight: 600;
  white-space: nowrap;
}

/* 主内容区 */
.main-content {
  display: flex;
  gap: 24px;
  width: 100%;
  height: 100%;
  min-height: 300px;
}

/* 左侧功能栏 */
.function-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: clamp(160px, 20vw, 200px);
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  box-sizing: border-box;
}

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
  background-color: #2196F3;
  color: white;
  font-weight: 500;
}

.function-item:not(.active):hover {
  background-color: #f5f5f5;
  color: #2196F3;
}

/* 右侧内容区 */
.content-area {
  flex: 1;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
}

.content-section {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  color: #333;
  font-size: 1.5rem;
  margin: 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

/* 接口列表内容样式 */
.interface-list-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

/* 接口卡片 */
.interface-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 请求头部 */
.request-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
}

.method-selector {
  min-width: 100px;
}

.method-dropdown {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.method-dropdown:focus {
  outline: none;
  border-color: #2196F3;
}

.url-input-group {
  flex: 1;
  display: flex;
  align-items: center;
  min-width: 300px;
}

.host-input {
  width: 250px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 0.9rem;
  border-right: none;
}

.url-separator {
  color: #999;
  padding: 0 4px;
}

.endpoint-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 0 4px 4px 0;
  font-size: 0.9rem;
}

.host-input:focus, .endpoint-input:focus {
  outline: none;
  border-color: #2196F3;
}

.send-btn {
  padding: 8px 16px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.send-btn:hover {
  background-color: #0c7cd5;
}

.send-icon {
  font-weight: bold;
}

/* 请求标签页 */
.request-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  background-color: #fafafa;
}

.tab-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.tab-item.active {
  border-bottom-color: #2196F3;
  color: #2196F3;
  font-weight: 500;
  background-color: white;
}

.tab-item:hover:not(.active) {
  background-color: #f0f0f0;
}

/* 标签页内容 */
.tab-content {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}

/* 参数内容 */
.params-content, .headers-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.params-table, .headers-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.params-header, .header-header {
  display: flex;
  gap: 8px;
  padding: 8px 0;
  font-weight: 500;
  color: #666;
  font-size: 0.85rem;
}

.param-column, .header-column {
  flex: 1;
}

.param-column:first-child, .header-column:first-child {
  flex: 1;
}

.param-column:nth-child(2), .header-column:nth-child(2) {
  flex: 1;
}

.param-column:nth-child(3) {
  flex: 1.5;
}

.param-column:last-child, .header-column:last-child {
  width: 40px;
  flex: none;
}

.param-row, .header-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.param-input, .header-input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.param-input:first-child, .header-input:first-child {
  flex: 1;
}

.param-input:nth-child(2) {
  flex: 1;
}

.param-input:nth-child(3) {
  flex: 1.5;
}

/* 按钮样式 */
.add-btn {
  align-self: flex-start;
  padding: 6px 12px;
  background-color: #f5f5f5;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background-color: #e9e9e9;
}

.remove-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: white;
  color: #999;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  padding: 0;
}

.remove-btn:hover {
  background-color: #f8d7da;
  color: #721c24;
  border-color: #f5c6cb;
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 请求体内容 */
.body-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.body-type-selector {
  display: flex;
  gap: 4px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.body-type-item {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.body-type-item.active {
  background-color: #e3f2fd;
  border-color: #bbdefb;
  color: #1565c0;
}

.body-type-item:hover:not(.active) {
  background-color: #f5f5f5;
}

.raw-body-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.raw-type-selector {
  align-self: flex-start;
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.8rem;
}

.raw-body-input {
  width: 100%;
  min-height: 200px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9rem;
  resize: vertical;
  box-sizing: border-box;
}

.form-data-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-data-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-data-header {
  display: flex;
  gap: 8px;
  padding: 8px 0;
  font-weight: 500;
  color: #666;
  font-size: 0.85rem;
}

.form-data-column {
  flex: 1;
}

.form-data-column:first-child, .form-data-column:nth-child(2) {
  flex: 2;
}

.form-data-column:nth-child(3) {
  width: 100px;
  flex: none;
}

.form-data-column:last-child {
  width: 40px;
  flex: none;
}

.form-data-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.form-data-input {
  flex: 2;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.form-data-type {
  width: 100px;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.form-data-file {
  flex: 2;
  padding: 6px 0;
  font-size: 0.9rem;
}

.body-placeholder, .auth-placeholder {
  padding: 40px 20px;
  text-align: center;
  color: #888;
  background-color: #fafafa;
  border-radius: 4px;
}

/* 认证内容 */
.auth-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.auth-type-selector {
  align-self: flex-start;
}

.auth-type-dropdown {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.auth-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 4px;
}

.auth-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.auth-field label {
  font-size: 0.85rem;
  color: #666;
}

.auth-input {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* 响应区域 */
.response-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 300px;
}

.response-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
  gap: 12px;
}

.response-status {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.9rem;
}

.status-code {
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  color: white;
}

.status-code.success {
  background-color: #4caf50;
}

.status-code.redirect {
  background-color: #ff9800;
}

.status-code.client-error {
  background-color: #f44336;
}

.status-code.server-error {
  background-color: #9e9e9e;
}

.response-time, .response-size {
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.response-tabs {
  display: flex;
  gap: 4px;
}

.response-tab-item {
  padding: 6px 12px;
  font-size: 0.85rem;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.response-tab-item.active {
  background-color: white;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.response-tab-item:hover:not(.active) {
  background-color: #e9e9e9;
}

.response-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.response-action-btn {
  padding: 4px 8px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.response-action-btn:hover {
  background-color: #f5f5f5;
}

.response-view-select {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

/* 响应内容 */
.response-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.response-body {
  margin: 0;
  color: #333;
  font-family: monospace;
  white-space: pre;
  overflow-x: auto;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  padding: 16px;
  border-radius: 4px;
  margin: 0;
  border: 1px solid #f5c6cb;
}

.empty-response, .empty-section {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
  background-color: #fafafa;
  border-radius: 4px;
  margin: 0;
}

/* 响应头和Cookies样式 */
.response-headers, .response-cookies {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.headers-list, .cookies-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-item, .cookie-item {
  display: flex;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 0.9rem;
}

.header-key, .cookie-name {
  font-weight: 500;
  margin-right: 8px;
  color: #2c3e50;
  min-width: 150px;
}

.header-value, .cookie-value {
  color: #34495e;
  word-break: break-all;
}

/* 时间线样式 */
.response-timeline {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.timeline-chart {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.timeline-bar {
  height: 30px;
  display: flex;
  width: 100%;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.timeline-segment {
  height: 100%;
  transition: width 0.5s ease;
}

.timeline-segment.dns {
  background-color: #42a5f5;
}

.timeline-segment.connect {
  background-color: #66bb6a;
}

.timeline-segment.send {
  background-color: #ec407a;
}

.timeline-segment.wait {
  background-color: #ffa726;
}

.timeline-segment.receive {
  background-color: #26c6da;
}

.timeline-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.timeline-stat {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  min-width: 100px;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
}

.stat-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
}

/* 测试用例样式 */
.test-case-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.test-case-actions {
  align-self: flex-start;
  margin-bottom: 10px;
}

.test-case-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.test-case-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
  position: relative;
  transition: box-shadow 0.3s;
}

.test-case-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.test-case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.test-case-title {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.test-case-body {
  color: #666;
  line-height: 1.6;
}

.empty-test-case {
  color: #888;
  text-align: center;
  padding: 40px 0;
  background-color: #fafafa;
  border-radius: 8px;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-item {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.9rem;
  color: #666;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #2196F3;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background-color: #f5f5f5;
}

.confirm-btn {
  padding: 6px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.confirm-btn:hover {
  background-color: #0c7cd5;
}

/* 其他功能区占位符 */
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
.function-sidebar::-webkit-scrollbar,
.tab-content::-webkit-scrollbar,
.response-content::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.content-area::-webkit-scrollbar-track,
.function-sidebar::-webkit-scrollbar-track,
.tab-content::-webkit-scrollbar-track,
.response-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.content-area::-webkit-scrollbar-thumb,
.function-sidebar::-webkit-scrollbar-thumb,
.tab-content::-webkit-scrollbar-thumb,
.response-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.content-area::-webkit-scrollbar-thumb:hover,
.function-sidebar::-webkit-scrollbar-thumb:hover,
.tab-content::-webkit-scrollbar-thumb:hover,
.response-content::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .url-input-group {
    min-width: 200px;
  }

  .host-input {
    width: 180px;
  }
}

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

  .request-header {
    flex-direction: column;
    align-items: stretch;
  }

  .method-selector {
    width: 100%;
  }

  .method-dropdown {
    width: 100%;
  }

  .url-input-group {
    width: 100%;
    min-width: auto;
  }

  .host-input {
    width: 40%;
  }

  .send-btn {
    width: 100%;
    justify-content: center;
  }

  .response-header {
    flex-direction: column;
    align-items: stretch;
  }

  .response-status, .response-tabs, .response-actions {
    width: 100%;
  }

  .response-tabs {
    overflow-x: auto;
    padding-bottom: 8px;
  }

  .timeline-stats {
    flex-direction: column;
  }

  .timeline-stat {
    width: 100%;
    min-width: auto;
  }
}
</style>