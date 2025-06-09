import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 配置axios默认值
axios.defaults.withCredentials = true // 允许跨域携带cookie

// 创建Vue应用实例
const app = createApp(App)

// 全局配置
app.config.globalProperties.$axios = axios

// 使用插件
app.use(ElementPlus)
app.use(router)

app.mount('#app') 