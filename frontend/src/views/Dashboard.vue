<template>
  <div class="dashboard-container">
    <el-menu
      mode="horizontal"
      :router="true"
      class="nav-menu"
    >
      <el-menu-item index="/dashboard">
        <el-icon><Monitor /></el-icon>
        Dashboard
      </el-menu-item>
      <el-menu-item index="/alerts">
        <el-icon><Bell /></el-icon>
        Alerts
      </el-menu-item>
      
      <!-- Crop Selector -->
      <div class="crop-selector-container">
        <el-select
          v-model="selectedCrop"
          placeholder="Select Crop"
          class="crop-selector"
          @change="handleCropChange"
        >
          <el-option
            v-for="crop in crops"
            :key="crop.id"
            :label="crop.name"
            :value="crop.id"
          />
        </el-select>
        <el-tooltip content="Crop Settings">
          <el-button
            class="settings-button"
            :icon="Setting"
            circle
            @click="showSettings = true"
          />
        </el-tooltip>
      </div>

      <div style="flex-grow: 1;"></div>
      
      <el-sub-menu index="2">
        <template #title>
          <el-icon><User /></el-icon>
          Admin
        </template>
        <el-menu-item @click="handleCommand('logout')">
          <el-icon><SwitchButton /></el-icon>
          Logout
        </el-menu-item>
      </el-sub-menu>
    </el-menu>

    <div class="dashboard-header">
      <h2>Sensor Monitoring Dashboard</h2>
      <div class="header-controls">
        <el-button type="primary" :loading="loading" @click="refresh">
          <el-icon><Refresh /></el-icon>
          Refresh Data
        </el-button>
      </div>
    </div>

    <!-- Sensor Cards -->
    <el-row :gutter="20" class="sensor-cards">
      <el-col :span="6" v-for="sensor in sensors" :key="sensor.id">
        <el-card class="sensor-card" :body-style="{ padding: '20px' }">
          <template #header>
            <div class="card-header">
              <span class="sensor-name">{{ sensor.name }}</span>
              <el-tag :type="sensor.status === 'active' ? 'success' : 'danger'" size="small">
                {{ sensor.status === 'active' ? 'Online' : 'Offline' }}
              </el-tag>
            </div>
          </template>
          <div class="sensor-content">
            <div class="sensor-icon-container">
              <img :src="getSensorIcon(sensor.type)" :alt="sensor.type" class="sensor-icon">
            </div>
            <div class="sensor-info">
              <div class="sensor-value">
                <span class="value">{{ sensor.current_value }}</span>
                <span class="unit">{{ getUnit(sensor.type) }}</span>
              </div>
              <div class="sensor-details">
                <p class="detail-item"><small>📍 {{ sensor.location }}</small></p>
                <p class="detail-item"><small>🕒 {{ sensor.last_update }}</small></p>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Data Charts -->
    <div class="charts-section">
      <h3>Sensor Data Trends</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="chart-container" ref="temperatureChart"></div>
        </el-col>
        <el-col :span="12">
          <div class="chart-container" ref="humidityChart"></div>
        </el-col>
        <el-col :span="12">
          <div class="chart-container" ref="lightChart"></div>
        </el-col>
        <el-col :span="12">
          <div class="chart-container" ref="soilChart"></div>
        </el-col>
      </el-row>
    </div>

    <!-- Crop Settings Dialog -->
    <crop-settings
      v-model="showSettings"
      @refresh="handleSettingsRefresh"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor, Bell, Setting, User, SwitchButton, Refresh } from '@element-plus/icons-vue'
import { useSensorData } from '@/hooks/useSensorData'
import * as echarts from 'echarts'
import CropSettings from '@/components/CropSettings.vue'

// 导入图标
import temperatureIcon from '@/assets/logo/temperature.png'
import humidityIcon from '@/assets/logo/humidity.png'
import lightIcon from '@/assets/logo/light.png'
import soilIcon from '@/assets/logo/soil.png'

const router = useRouter()
const { sensors, loading, historyData, refresh } = useSensorData()

// 作物选择相关
const crops = ref([])
const selectedCrop = ref(null)
const showSettings = ref(false)

// 获取所有作物类型
const fetchCrops = async () => {
  try {
    const response = await fetch('/api/crops')
    const data = await response.json()
    crops.value = data
    if (data.length > 0 && !selectedCrop.value) {
      selectedCrop.value = data[0].id
      updateChartThresholds(data[0])
    }
  } catch (error) {
    console.error('Failed to fetch crop types:', error)
  }
}

// 处理作物变更
const handleCropChange = (cropId) => {
  const crop = crops.value.find(c => c.id === cropId)
  if (crop) {
    updateChartThresholds(crop)
  }
}

// 处理设置更新
const handleSettingsRefresh = () => {
  fetchCrops()
}

// 更新图表阈值
const updateChartThresholds = (crop) => {
  // ... existing updateCharts code ...
  // 使用 crop.thresholds 替代之前的 cropThresholds[selectedCrop.value]
}

// 图表实例引用
const temperatureChart = ref(null)
const humidityChart = ref(null)
const lightChart = ref(null)
const soilChart = ref(null)

// 图表实例
let charts = {
  temperature: null,
  humidity: null,
  light: null,
  soil: null
}

// 获取传感器单位
const getUnit = (type) => {
  const units = {
    'temperature': '°C',
    'humidity': '%',
    'light': 'lux',
    'ph': 'pH'
  }
  return units[type.toLowerCase()] || ''
}

// 获取传感器对应的图标
const getSensorIcon = (type) => {
  const icons = {
    'temperature': temperatureIcon,
    'humidity': humidityIcon,
    'light': lightIcon,
    'ph': soilIcon
  }
  return icons[type.toLowerCase()] || temperatureIcon
}

// 生成阈值数据
const generateThresholdData = (type, timeData) => {
  const crop = crops.value.find(c => c.id === selectedCrop.value)
  if (!crop) return timeData.map(() => ({ min: 0, max: 0 }))

  return timeData.map(time => {
    const hour = new Date(time).getHours()
    const isDay = hour >= 6 && hour < 18 // 假设6点到18点是白天
    return crop.thresholds[type.toLowerCase()][isDay ? 'day' : 'night']
  })
}

// 检查数据是否超出阈值
const isDataOutOfRange = (value, type, time) => {
  const crop = crops.value.find(c => c.id === selectedCrop.value)
  if (!crop) return false

  const hour = new Date(time).getHours()
  const isDay = hour >= 6 && hour < 18
  const threshold = crop.thresholds[type.toLowerCase()][isDay ? 'day' : 'night']
  return value < threshold.min || value > threshold.max
}

// 更新图表
const updateCharts = () => {
  if (!charts.temperature || !historyData.value || !selectedCrop.value) return

  const timeData = historyData.value.temperature.map(item => item.time)
  const crop = crops.value.find(c => c.id === selectedCrop.value)
  if (!crop) return

  // 更新温度图表
  if (historyData.value.temperature) {
    const tempThresholds = generateThresholdData('temperature', timeData)
    charts.temperature.setOption({
      xAxis: {
        data: timeData
      },
      series: [
        {
          data: historyData.value.temperature.map(item => item.value),
          itemStyle: {
            color: function(params) {
              return isDataOutOfRange(params.data, 'temperature', timeData[params.dataIndex]) ? '#ff4444' : '#409EFF'
            }
          }
        },
        {
          name: 'Max Threshold',
          type: 'line',
          data: tempThresholds.map(t => t.max),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        },
        {
          name: 'Min Threshold',
          type: 'line',
          data: tempThresholds.map(t => t.min),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        }
      ]
    })
  }

  // 更新湿度图表
  if (historyData.value.humidity) {
    const humidityThresholds = generateThresholdData('humidity', timeData)
    charts.humidity.setOption({
      xAxis: {
        data: timeData
      },
      series: [
        {
          data: historyData.value.humidity.map(item => item.value),
          itemStyle: {
            color: function(params) {
              return isDataOutOfRange(params.data, 'humidity', timeData[params.dataIndex]) ? '#ff4444' : '#409EFF'
            }
          }
        },
        {
          name: 'Max Threshold',
          type: 'line',
          data: humidityThresholds.map(t => t.max),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        },
        {
          name: 'Min Threshold',
          type: 'line',
          data: humidityThresholds.map(t => t.min),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        }
      ]
    })
  }

  // 更新光照图表
  if (historyData.value.light) {
    const lightThresholds = generateThresholdData('light', timeData)
    charts.light.setOption({
      xAxis: {
        data: timeData
      },
      series: [
        {
          data: historyData.value.light.map(item => item.value),
          itemStyle: {
            color: function(params) {
              return isDataOutOfRange(params.data, 'light', timeData[params.dataIndex]) ? '#ff4444' : '#409EFF'
            }
          }
        },
        {
          name: 'Max Threshold',
          type: 'line',
          data: lightThresholds.map(t => t.max),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        },
        {
          name: 'Min Threshold',
          type: 'line',
          data: lightThresholds.map(t => t.min),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        }
      ]
    })
  }

  // 更新土壤pH图表
  if (historyData.value.soil_moisture) {
    const soilThresholds = generateThresholdData('soil', timeData)
    charts.soil.setOption({
      xAxis: {
        data: timeData
      },
      series: [
        {
          data: historyData.value.soil_moisture.map(item => item.value),
          itemStyle: {
            color: function(params) {
              return isDataOutOfRange(params.data, 'soil', timeData[params.dataIndex]) ? '#ff4444' : '#409EFF'
            }
          }
        },
        {
          name: 'Max Threshold',
          type: 'line',
          data: soilThresholds.map(t => t.max),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        },
        {
          name: 'Min Threshold',
          type: 'line',
          data: soilThresholds.map(t => t.min),
          lineStyle: {
            type: 'dashed',
            color: '#ff4444'
          },
          symbol: 'none'
        }
      ]
    })
  }
}

// 初始化图表
const initCharts = () => {
  // 温度图表
  charts.temperature = echarts.init(temperatureChart.value)
  charts.temperature.setOption({
    title: {
      text: 'Temperature Changes',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const time = params[0].axisValue
        const value = params[0].data
        const selectedCropData = crops.value.find(c => c.id === selectedCrop.value)
        if (!selectedCropData) return `${time}<br/>Temperature: ${value}°C`
        
        const threshold = selectedCropData.thresholds.temperature[new Date(time).getHours() >= 6 && new Date(time).getHours() < 18 ? 'day' : 'night']
        const isOutOfRange = isDataOutOfRange(value, 'temperature', time)
        let warning = isOutOfRange ? '<br/><span style="color: red">⚠️ Warning: Value out of range!</span>' : ''
        return `${time}<br/>Temperature: ${value}°C${warning}<br/>Threshold: ${threshold.min}°C - ${threshold.max}°C`
      }
    },
    grid: {
      top: 60,
      bottom: 80,
      left: 60,
      right: 20
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          return value
        }
      }
    },
    yAxis: {
      type: 'value',
      name: 'Temperature (°C)',
      nameTextStyle: {
        fontSize: 12
      },
      axisLabel: {
        fontSize: 12
      }
    },
    series: [
      {
        name: 'Temperature',
        type: 'line',
        data: [],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ],
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 100,
        bottom: 10
      },
      {
        type: 'inside'
      }
    ]
  })

  // 湿度图表
  charts.humidity = echarts.init(humidityChart.value)
  charts.humidity.setOption({
    title: {
      text: 'Humidity Changes',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const time = params[0].axisValue
        const value = params[0].data
        const selectedCropData = crops.value.find(c => c.id === selectedCrop.value)
        if (!selectedCropData) return `${time}<br/>Humidity: ${value}%`
        
        const threshold = selectedCropData.thresholds.humidity[new Date(time).getHours() >= 6 && new Date(time).getHours() < 18 ? 'day' : 'night']
        const isOutOfRange = isDataOutOfRange(value, 'humidity', time)
        let warning = isOutOfRange ? '<br/><span style="color: red">⚠️ Warning: Value out of range!</span>' : ''
        return `${time}<br/>Humidity: ${value}%${warning}<br/>Threshold: ${threshold.min}% - ${threshold.max}%`
      }
    },
    grid: {
      top: 60,
      bottom: 80,
      left: 60,
      right: 20
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          return value
        }
      }
    },
    yAxis: {
      type: 'value',
      name: 'Humidity (%)',
      nameTextStyle: {
        fontSize: 12
      },
      axisLabel: {
        fontSize: 12
      }
    },
    series: [
      {
        name: 'Humidity',
        type: 'line',
        data: [],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ],
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 100,
        bottom: 10
      },
      {
        type: 'inside'
      }
    ]
  })

  // 光照图表
  charts.light = echarts.init(lightChart.value)
  charts.light.setOption({
    title: {
      text: 'Light Changes',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const time = params[0].axisValue
        const value = params[0].data
        const selectedCropData = crops.value.find(c => c.id === selectedCrop.value)
        if (!selectedCropData) return `${time}<br/>Light: ${value}lux`
        
        const threshold = selectedCropData.thresholds.light[new Date(time).getHours() >= 6 && new Date(time).getHours() < 18 ? 'day' : 'night']
        const isOutOfRange = isDataOutOfRange(value, 'light', time)
        let warning = isOutOfRange ? '<br/><span style="color: red">⚠️ Warning: Value out of range!</span>' : ''
        return `${time}<br/>Light: ${value}lux${warning}<br/>Threshold: ${threshold.min}lux - ${threshold.max}lux`
      }
    },
    grid: {
      top: 60,
      bottom: 80,
      left: 60,
      right: 20
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          return value
        }
      }
    },
    yAxis: {
      type: 'value',
      name: 'Light (lux)',
      nameTextStyle: {
        fontSize: 12
      },
      axisLabel: {
        fontSize: 12
      }
    },
    series: [
      {
        name: 'Light',
        type: 'line',
        data: [],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ],
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 100,
        bottom: 10
      },
      {
        type: 'inside'
      }
    ]
  })

  // 土壤pH图表
  charts.soil = echarts.init(soilChart.value)
  charts.soil.setOption({
    title: {
      text: 'Soil pH Changes',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const time = params[0].axisValue
        const value = params[0].data
        const selectedCropData = crops.value.find(c => c.id === selectedCrop.value)
        if (!selectedCropData) return `${time}<br/>Soil pH: ${value}`
        
        const threshold = selectedCropData.thresholds.soil[new Date(time).getHours() >= 6 && new Date(time).getHours() < 18 ? 'day' : 'night']
        const isOutOfRange = isDataOutOfRange(value, 'soil', time)
        let warning = isOutOfRange ? '<br/><span style="color: red">⚠️ Warning: Value out of range!</span>' : ''
        return `${time}<br/>Soil pH: ${value}${warning}<br/>Threshold: ${threshold.min} - ${threshold.max}`
      }
    },
    grid: {
      top: 60,
      bottom: 80,
      left: 60,
      right: 20
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          return value
        }
      }
    },
    yAxis: {
      type: 'value',
      name: 'Soil pH',
      nameTextStyle: {
        fontSize: 12
      },
      axisLabel: {
        fontSize: 12
      }
    },
    series: [
      {
        name: 'Soil pH',
        type: 'line',
        data: [],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ],
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 100,
        bottom: 10
      },
      {
        type: 'inside'
      }
    ]
  })

  updateCharts()
}

// 监听作物选择变化
watch(selectedCrop, () => {
  updateCharts()
})

// 监听历史数据变化
watch(historyData, () => {
  updateCharts()
}, { deep: true })

// 监听窗口大小变化
const handleResize = () => {
  Object.values(charts).forEach(chart => {
    chart && chart.resize()
  })
}

onMounted(() => {
  fetchCrops()
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  Object.values(charts).forEach(chart => {
    chart && chart.dispose()
  })
})

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('isLoggedIn')
    router.push('/login')
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-controls {
  display: flex;
  gap: 20px;
  align-items: center;
}

.crop-selector {
  width: 200px;
}

.dashboard-header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.sensor-cards {
  margin-bottom: 30px;
}

.sensor-card {
  margin-bottom: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.sensor-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sensor-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #303133;
}

.sensor-content {
  display: flex;
  align-items: center;
  gap: 20px;
  min-height: 120px;
}

.sensor-icon-container {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sensor-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.sensor-info {
  flex: 1;
}

.sensor-value {
  text-align: right;
  margin: 10px 0;
  font-family: 'Comic Sans MS', 'Comic Sans', cursive;
}

.sensor-value .value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #000000;
}

.sensor-value .unit {
  font-size: 1.2rem;
  color: #000000;
  margin-left: 4px;
  opacity: 0.8;
}

.sensor-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
  text-align: right;
}

.detail-item {
  margin: 0;
  color: #909399;
}

.detail-item small {
  font-size: 0.85rem;
}

.charts-section {
  margin-top: 40px;
}

.charts-section h3 {
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
  font-size: 18px;
  font-weight: 600;
}

.chart-container {
  height: 300px;
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  box-sizing: border-box;
}

.chart-container .echarts-title {
  font-size: 16px;
  margin-bottom: 10px;
}

.chart-container .echarts-axis-label {
  font-size: 12px;
}

.nav-menu {
  padding: 0 20px;
}

.crop-selector-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  gap: 10px;
}

.settings-button {
  padding: 8px;
}
</style>