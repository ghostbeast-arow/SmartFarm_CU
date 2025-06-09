<template>
  <div class="login-container">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="particles"></div>
      <div class="gradient-overlay"></div>
    </div>

    <!-- 左侧内容区 -->
    <div class="left-content">
      <!-- 项目简介 -->
      <div class="project-info">
        <h1>Smart Farm System</h1>
        <h2>Welcome to the next generation of agricultural technology. Our Smart Farm System leverages IoT sensors, real-time analytics, and automated controls to revolutionize farming practices. Experience precision agriculture at its finest with our comprehensive monitoring and management solution.</h2>
        <div class="features">
          <div class="feature">
            <i class="el-icon-monitor"></i>
            <span>Real-time Monitoring</span>
          </div>
          <div class="feature">
            <i class="el-icon-data-analysis"></i>
            <span>Data Analytics</span>
          </div>
          <div class="feature">
            <i class="el-icon-setting"></i>
            <span>Automated Control</span>
          </div>
        </div>
      </div>

      <!-- 团队成员展示 -->
      <div class="team-section">
        <el-carousel :interval="4000" type="card" height="500px">
          <el-carousel-item v-for="member in teamMembers" :key="member.id">
            <div class="team-card">
              <img :src="member.photo" :alt="member.name">
              <h3>{{ member.name }}</h3>
              <p>{{ member.role }}</p>
              <p>{{ member.description }}</p>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="login-form-container">
      <el-card class="login-card">
        <template #header>
          <h2>Smart Farm System</h2>
        </template>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="Username"
              prefix-icon="el-icon-user"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="Password"
              show-password
              prefix-icon="el-icon-lock"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">
              Login
            </el-button>
          </el-form-item>
          <div class="form-footer">
            <el-button type="text" @click="showSignUpDialog">Sign Up</el-button>
            <el-button type="text" @click="showForgotPasswordDialog">Forgot Password?</el-button>
          </div>
        </el-form>
      </el-card>
    </div>

    <!-- 注册弹窗 -->
    <el-dialog v-model="signUpDialogVisible" title="Sign Up" width="30%">
      <el-form :model="signUpForm" :rules="signUpRules" ref="signUpFormRef">
        <el-form-item prop="username">
          <el-input v-model="signUpForm.username" placeholder="Username" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="signUpForm.email" placeholder="Email" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="signUpForm.password" type="password" placeholder="Password" />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="signUpForm.confirmPassword" type="password" placeholder="Confirm Password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="signUpDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="handleSignUp">Sign Up</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 忘记密码弹窗 -->
    <el-dialog v-model="forgotPasswordDialogVisible" title="Reset Password" width="30%">
      <el-form :model="forgotPasswordForm" :rules="forgotPasswordRules" ref="forgotPasswordFormRef">
        <el-form-item prop="email">
          <el-input v-model="forgotPasswordForm.email" placeholder="Enter your email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="forgotPasswordDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="handleForgotPassword">Submit</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const signUpFormRef = ref(null)
const forgotPasswordFormRef = ref(null)
const loading = ref(false)
const signUpDialogVisible = ref(false)
const forgotPasswordDialogVisible = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const signUpForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const forgotPasswordForm = reactive({
  email: ''
})

const rules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' }
  ]
}

const signUpRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: 'Please confirm password', trigger: 'blur' }
  ]
}

const forgotPasswordRules = {
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' }
  ]
}

const teamMembers = ref([
  {
    id: 1,
    name: 'Binyuan Zhao',
    role: 'Development Engineer',
    description: 'Lead System Architect and Full-stack Developer, responsible for overall system design and development',
    photo: '/team/binyuan.jpg'
  },
  {
    id: 2,
    name: 'Vasile Palade',
    role: 'Advisor',
    description: 'Special thanks to Vasile Palade for his excellent guidance and support. His expertise was crucial to our project\'s success.',
    photo: '/team/VasilePalade.jpg'
  },
  {
    id: 3,
    name: 'Xinfei Dong',
    role: 'Project Strategist',
    description: 'Carry out project database design, develop the project strategic, and design the delivery of presentation materials.',
    photo: '/team/xinfei.jpg'
  },
  {
    id: 4,
    name: 'Weihang Song',
    role: 'Data analyst',
    description: 'Deploy and maintain MQTT Broker, configure Topic structure. Design database structure and realize data persistence',
    photo: '/team/weihang.jpg'
  },
  {
    id: 5,
    name: 'Muhammad Aleem',
    role: 'Advisor',
    description: 'Special thanks to Muhammad Aleem for his excellent guidance and support. His expertise was crucial to our project\'s success.',
    photo: '/team/MuhammadAleem.png'
  },
  {
    id: 6,
    name: 'Yanqi Wang',
    role: 'Project Leader',
    description: 'Led cross-functional coordination, ensured timely progress across all project phases, and oversaw the execution of key deliverables with strategic vision',
    photo: '/team/yanqi.jpg'
  }
])

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const response = await axios.post('/api/login', {
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (response.data.success) {
      ElMessage.success('Login successful')
      localStorage.setItem('isLoggedIn', 'true')
      router.push('/dashboard')
    }
  } catch (error) {
    if (error.response?.status === 401) {
      ElMessage.error('Invalid credentials')
    } else {
      ElMessage.error('Login failed')
    }
  } finally {
    loading.value = false
  }
}

const showSignUpDialog = () => {
  signUpDialogVisible.value = true
}

const showForgotPasswordDialog = () => {
  forgotPasswordDialogVisible.value = true
}

const handleSignUp = () => {
  // 这里只做前端展示，不实现实际注册逻辑
  ElMessage.success('Sign up form submitted (demo only)')
  signUpDialogVisible.value = false
}

const handleForgotPassword = () => {
  // 这里只做前端展示，不实现实际重置密码逻辑
  ElMessage.success('Password reset email sent (demo only)')
  forgotPasswordDialogVisible.value = false
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: grid;
  grid-template-columns: 1fr 450px;
  position: relative;
  overflow: hidden;
  background-color: #1a1a1a;
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(135deg, #1a1a1a, #2d3436);
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(66, 190, 165, 0.3),
    rgba(41, 128, 185, 0.3),
    rgba(142, 68, 173, 0.3));
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  mix-blend-mode: soft-light;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gradient-overlay {
  display: none;
}

.left-content {
  grid-column: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 2rem;
  gap: 2rem;
  overflow-y: auto;
}

.project-info {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  max-width: 800px;
  margin: 0 auto;
  background: rgba(188, 201, 181, 0.288);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.team-section {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.login-form-container {
  grid-column: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  height: 100vh;
}

.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.login-card :deep(.el-card__header) {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px;
}

.login-card h2 {
  color: #fff;
  font-size: 28px;
  text-align: center;
  margin: 0;
  letter-spacing: 1px;
}

.login-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.login-card :deep(.el-form) {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-card :deep(.el-input__inner) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

.login-card :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.5);
}

.login-card :deep(.el-button--primary) {
  background: linear-gradient(135deg, #42bea5, #2980b9);
  border: none;
  width: 100%;
  height: 40px;
  font-size: 18px;
  letter-spacing: 1px;
}

.login-card :deep(.el-button--text) {
  color: rgba(255, 255, 255, 0.7);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 1rem;
  justify-content: center;
  align-items: center;
}

.feature {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 15px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.feature:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.1);
}

.feature i {
  font-size: 16px;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #42bea5, #2980b9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature span {
  color: rgb(0, 0, 0);
  font-size: 20px;
}

:deep(.el-carousel) {
  width: 100%;
  height: 100%;
}

:deep(.el-carousel__container) {
  height: 100%;
}

:deep(.el-carousel__item) {
  padding: 1rem;
}

:deep(.el-carousel__item--card) {
  width: 50%;
}

:deep(.el-carousel__item--card.is-active) {
  z-index: 10;
}

.team-card {
  height: 100%;
  background: #ffffff;  /* 设置不透明的白色背景 */
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.team-card img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #409EFF;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.team-card h3 {
  color: #333333;
  font-size: 1.5rem;
  margin-bottom: 18px;
  margin-top: 15px;
}

.team-card p {
  color: #666666;
  margin: 0.5rem 0;
  line-height: 1.5;
}

:deep(.el-carousel__item--card.is-active .team-card) {
  transform: scale(1.05);
}

:deep(.el-dialog) {
  background: #1a1a1a;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-dialog__header) {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px;
}

:deep(.el-dialog__title) {
  color: #fff;
}

:deep(.el-dialog__body) {
  padding: 30px;
  color: #fff;
}

:deep(.el-dialog__footer) {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-dialog .el-input__inner) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

:deep(.el-dialog .el-button--primary) {
  background: linear-gradient(135deg, #42bea5, #2980b9);
  border: none;
}

:deep(.el-dialog .el-button--default) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
}
</style> 