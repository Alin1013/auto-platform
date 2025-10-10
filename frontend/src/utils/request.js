import axios from 'axios';

const request = axios.create({
  baseURL: 'http://localhost:8000/api',  // 后端API基础地址
  timeout: 5000
});

// 请求拦截器（添加Token）
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器（处理Token过期）
request.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      try {
        const res = await axios.post('http://localhost:8000/api/core/token/refresh/', {
          refresh: refreshToken
        });
        localStorage.setItem('access_token', res.data.access);
        return request(originalRequest);
      } catch (err) {
        // 刷新Token失败，跳转登录
        window.location.href = '/#/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default request;