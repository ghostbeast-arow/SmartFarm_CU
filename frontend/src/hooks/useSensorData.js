import { ref, onMounted, onUnmounted } from 'vue'
import { getSensors, getSensorHistory } from '@/api/sensor'
import { ElMessage } from 'element-plus'

export function useSensorData() {
  const sensors = ref([])
  const loading = ref(false)
  const refreshInterval = ref(null)
  const historyData = ref({
    temperature: [],
    humidity: [],
    light: [],
    soil_moisture: []
  })

  // 获取历史数据
  const fetchHistory = async () => {
    try {
      const response = await getSensorHistory()
      if (response && response.data) {
        historyData.value = response.data
        console.log('Successfully fetched history data:', {
          timestamp: new Date().toLocaleString(),
          data: historyData.value
        })
      } else {
        throw new Error('Invalid response format')
      }
    } catch (error) {
      console.error('Failed to fetch history data:', error)
      // 如果获取历史数据失败，使用空数组作为默认值
      historyData.value = {
        temperature: [],
        humidity: [],
        light: [],
        soil_moisture: []
      }
      // 只在非404错误时显示错误消息
      if (error.response && error.response.status !== 404) {
        ElMessage.error('获取历史数据失败，将使用空数据')
      }
    }
  }

  // 获取传感器数据
  const fetchSensors = async () => {
    if (loading.value) return // 防止重复请求
    
    loading.value = true
    try {
      const response = await getSensors()
      if (response && response.data) {
        sensors.value = response.data.map(sensor => ({
          ...sensor,
          name: sensor.name || 'Unnamed Sensor',
          type: sensor.type || 'Unknown Type',
          location: sensor.location || 'Unknown Location',
          status: sensor.status || 'inactive',
          last_update: sensor.last_update || 'Unknown Time',
          current_value: sensor.current_value || '--'
        }))
        
        // 更新历史数据
        const now = new Date().toLocaleString()
        sensors.value.forEach(sensor => {
          // 将传感器类型映射到历史数据的键名
          const typeMap = {
            'Temperature': 'temperature',
            'Humidity': 'humidity',
            'Light': 'light',
            'Soil': 'soil_moisture'
          }
          const dataKey = typeMap[sensor.type]
          
          if (dataKey && historyData.value[dataKey]) {
            let value = parseFloat(sensor.current_value) || 0
            // 对土壤pH值进行范围限制
            if (dataKey === 'soil_moisture') {
              value = Math.max(0, Math.min(14, value))
            }
            
            // 检查是否已存在相同时间的数据
            const existingIndex = historyData.value[dataKey].findIndex(
              item => item.time === now
            )
            
            if (existingIndex !== -1) {
              // 更新已存在的数据
              historyData.value[dataKey][existingIndex].value = value
            } else {
              // 添加新数据
              historyData.value[dataKey].push({
                time: now,
                value: value
              })
              // 只保留最近100个数据点
              if (historyData.value[dataKey].length > 100) {
                historyData.value[dataKey].shift()
              }
            }
          }
        })
        
        // 打印成功获取的数据
        console.log('Sensor data updated successfully:', {
          timestamp: now,
          totalSensors: sensors.value.length,
          activeSensors: sensors.value.filter(s => s.status === 'active').length,
          data: sensors.value
        })
      } else {
        throw new Error('Invalid response format')
      }
    } catch (error) {
      console.error('Failed to fetch sensor data:', error)
      ElMessage.error('获取传感器数据失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }

  // 开始定时刷新
  const startAutoRefresh = (interval = 5000) => {
    if (refreshInterval.value) {
      stopAutoRefresh() // 确保先清除之前的定时器
    }
    refreshInterval.value = setInterval(fetchSensors, interval)
    console.log(`Started auto-refresh, interval: ${interval}ms`)
  }

  // 停止定时刷新
  const stopAutoRefresh = () => {
    if (refreshInterval.value) {
      clearInterval(refreshInterval.value)
      refreshInterval.value = null
      console.log('Stopped auto-refresh')
    }
  }

  // 手动刷新
  const refresh = async () => {
    console.log('Manual refresh triggered')
    try {
      await fetchSensors()
      ElMessage.success('数据刷新成功')
    } catch (error) {
      console.error('Manual refresh failed:', error)
      ElMessage.error('数据刷新失败，请稍后重试')
    }
  }

  // 页面加载时获取数据并开始自动刷新
  onMounted(async () => {
    console.log('Component mounted, initializing data')
    try {
      // 先获取历史数据
      await fetchHistory()
      // 然后获取当前数据并开始自动刷新
      await fetchSensors()
      startAutoRefresh()
    } catch (error) {
      console.error('Initialization failed:', error)
      ElMessage.error('初始化数据失败，请刷新页面重试')
    }
  })

  // 页面卸载时清理定时器
  onUnmounted(() => {
    console.log('Component unmounted, cleaning up')
    stopAutoRefresh()
  })

  return {
    sensors,
    loading,
    historyData,
    refresh,
    startAutoRefresh,
    stopAutoRefresh
  }
} 