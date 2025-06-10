<template>
  <div class="alerts-container">
    <div class="alerts-header">
      <h2>Sensor Alerts</h2>
      <div class="header-controls">
        <el-button type="primary" :loading="loading" @click="refresh">
          <el-icon><Refresh /></el-icon>
          Refresh Alerts
        </el-button>
      </div>
    </div>

    <!-- 警报统计卡片 -->
    <el-row :gutter="20" class="alert-stats">
      <el-col :span="6">
        <el-card class="stat-card" :body-style="{ padding: '20px' }">
          <div class="stat-content">
            <div class="stat-icon temperature">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.temperature }}</div>
              <div class="stat-label">Temperature Alerts</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" :body-style="{ padding: '20px' }">
          <div class="stat-content">
            <div class="stat-icon humidity">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.humidity }}</div>
              <div class="stat-label">Humidity Alerts</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" :body-style="{ padding: '20px' }">
          <div class="stat-content">
            <div class="stat-icon light">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.light }}</div>
              <div class="stat-label">Light Alerts</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" :body-style="{ padding: '20px' }">
          <div class="stat-content">
            <div class="stat-icon soil">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.soil }}</div>
              <div class="stat-label"> pH Alerts</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 警报列表 -->
    <el-card class="alert-list">
      <template #header>
        <div class="alert-list-header">
          <span>Recent Alerts</span>
          <el-radio-group v-model="filterType" size="small">
            <el-radio-button label="all">All</el-radio-button>
            <el-radio-button label="temperature">Temperature</el-radio-button>
            <el-radio-button label="humidity">Humidity</el-radio-button>
            <el-radio-button label="light">Light</el-radio-button>
            <el-radio-button label="soil">Soil pH</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <el-table :data="filteredAlerts" style="width: 100%">
        <el-table-column prop="time" label="Time" width="180" />
        <el-table-column prop="type" label="Type" width="120">
          <template #default="{ row }">
            <el-tag :type="getAlertTagType(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sensor" label="Sensor" width="150" />
        <el-table-column prop="value" label="Value" width="120">
          <template #default="{ row }">
            {{ row.value }}{{ getUnit(row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="threshold" label="Threshold" width="180">
          <template #default="{ row }">
            {{ row.threshold.min }}{{ getUnit(row.type) }} - {{ row.threshold.max }}{{ getUnit(row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Status" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'danger' : 'info'">
              {{ row.status === 'active' ? 'Active' : 'Resolved' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="120">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'active'"
              type="primary"
              size="small"
              @click="handleResolve(row)"
            >
              Resolve
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Add Alert Dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="Add New Alert"
      width="500px"
    >
      <el-form :model="newAlert" label-width="120px">
        <el-form-item label="Alert Type">
          <el-select v-model="newAlert.type" placeholder="Select type">
            <el-option label="Temperature" value="Temperature" />
            <el-option label="Humidity" value="Humidity" />
            <el-option label="Water Level" value="Water Level" />
            <el-option label="System" value="System" />
          </el-select>
        </el-form-item>
        <el-form-item label="Message">
          <el-input v-model="newAlert.message" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitNewAlert">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Refresh, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 状态
const loading = ref(false)
const filterType = ref('all')

// 模拟的统计数据
const stats = ref({
  temperature: 3,
  humidity: 2,
  light: 1,
  soil: 2
})

// 模拟的警报数据
const alerts = ref([
  {
    id: 1,
    time: '2024-03-23 10:30:15',
    type: 'Temperature',
    sensor: 'Temperature Sensor 1',
    value: 32.5,
    threshold: { min: 20, max: 30 },
    status: 'active'
  },
  {
    id: 2,
    time: '2024-03-23 10:25:30',
    type: 'Humidity',
    sensor: 'Humidity Sensor 1',
    value: 95,
    threshold: { min: 50, max: 90 },
    status: 'active'
  },
  {
    id: 3,
    time: '2024-03-23 10:20:45',
    type: 'Light',
    sensor: 'Light Sensor 1',
    value: 1500,
    threshold: { min: 800, max: 1200 },
    status: 'resolved'
  },
  {
    id: 4,
    time: '2024-03-23 10:15:20',
    type: 'Soil',
    sensor: 'Soil Sensor 1',
    value: 8.5,
    threshold: { min: 6.0, max: 7.5 },
    status: 'active'
  },
  {
    id: 5,
    time: '2024-03-23 10:10:05',
    type: 'Temperature',
    sensor: 'Temperature Sensor 2',
    value: 18.5,
    threshold: { min: 20, max: 30 },
    status: 'active'
  }
])

// 根据类型过滤警报
const filteredAlerts = computed(() => {
  if (filterType.value === 'all') {
    return alerts.value
  }
  return alerts.value.filter(alert => 
    alert.type.toLowerCase() === filterType.value
  )
})

// 获取警报标签类型
const getAlertTagType = (type) => {
  const types = {
    'Temperature': 'danger',
    'Humidity': 'warning',
    'Light': 'info',
    'Soil': 'error'
  }
  return types[type] || 'info'
}

// 获取单位
const getUnit = (type) => {
  const units = {
    'Temperature': '°C',
    'Humidity': '%',
    'Light': 'lux',
    'Soil': 'pH'
  }
  return units[type] || ''
}

// 处理警报解决
const handleResolve = (alert) => {
  const index = alerts.value.findIndex(a => a.id === alert.id)
  if (index !== -1) {
    alerts.value[index].status = 'resolved'
    ElMessage.success('Alert resolved successfully')
  }
}

// 刷新数据
const refresh = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('Alerts refreshed')
  }, 1000)
}

const dialogVisible = ref(false)
const newAlert = ref({
  type: '',
  message: ''
})

// Audio elements
const alertSound = new Audio('/sounds/alert.mp3')
const resolveSound = new Audio('/sounds/resolve.mp3')

const handleAddAlert = () => {
  dialogVisible.value = true
  newAlert.value = {
    type: '',
    message: ''
  }
}

const submitNewAlert = () => {
  if (!newAlert.value.type || !newAlert.value.message) {
    ElMessage.warning('Please fill in all fields')
    return
  }

  const alert = {
    id: alerts.value.length + 1,
    type: newAlert.value.type,
    message: newAlert.value.message,
    timestamp: new Date().toLocaleString(),
    status: 'Active'
  }

  alerts.value.unshift(alert)
  dialogVisible.value = false
  
  // Play alert sound
  alertSound.play().catch(error => {
    console.error('Error playing alert sound:', error)
  })

  ElMessage.success('Alert added successfully')
}

const handleDeleteAlert = (alert) => {
  const index = alerts.value.findIndex(a => a.id === alert.id)
  if (index !== -1) {
    alerts.value.splice(index, 1)
    
    // Play resolve sound
    resolveSound.play().catch(error => {
      console.error('Error playing resolve sound:', error)
    })

    ElMessage.success('Alert deleted successfully')
  }
}
</script>

<style scoped>
.alerts-container {
  padding: 20px;
}

.alerts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.alerts-header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.header-controls {
  display: flex;
  gap: 20px;
  align-items: center;
}

.alert-stats {
  margin-bottom: 30px;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.temperature {
  background-color: #fef0f0;
  color: #f56c6c;
}

.stat-icon.humidity {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.light {
  background-color: #f0f9eb;
  color: #67c23a;
}

.stat-icon.soil {
  background-color: #f4f4f5;
  color: #909399;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-text-color-primary);
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.alert-list {
  margin-top: 20px;
}

.alert-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-list-header span {
  font-size: 16px;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 