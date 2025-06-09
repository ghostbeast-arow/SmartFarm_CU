import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: '', // 移除/api前缀，让vite代理处理
  timeout: 10000, // 增加超时时间到10秒
  retries: 3, // 添加重试次数
  retryDelay: 1000, // 重试延迟时间
  withCredentials: true, // 允许跨域携带cookie
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  async error => {
    const config = error.config
    
    // 如果没有设置重试配置，或者已经重试过了，就直接返回错误
    if (!config || !config.retries || config.__retryCount >= config.retries) {
      ElMessage.error(error.message || '请求失败')
      return Promise.reject(error)
    }
    
    // 设置重试次数
    config.__retryCount = config.__retryCount || 0
    config.__retryCount++
    
    // 延迟重试
    await new Promise(resolve => setTimeout(resolve, config.retryDelay))
    
    // 重新发起请求
    return service(config)
  }
)

export default service 