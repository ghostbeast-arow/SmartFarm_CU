import request from '@/utils/request'

// 获取所有传感器数据
export const getSensors = () => {
  return request({
    url: '/api/sensors',
    method: 'get'
  })
}

// 获取单个传感器数据
export const getSensorById = (id) => {
  return request({
    url: `/api/sensors/${id}`,
    method: 'get'
  })
}

// 添加传感器
export const addSensor = (data) => {
  return request({
    url: '/api/sensors',
    method: 'post',
    data
  })
}

// 更新传感器
export const updateSensor = (id, data) => {
  return request({
    url: `/api/sensors/${id}`,
    method: 'put',
    data
  })
}

// 删除传感器
export const deleteSensor = (id) => {
  return request({
    url: `/api/sensors/${id}`,
    method: 'delete'
  })
}

// 获取传感器历史数据
export function getSensorHistory(limit = 100) {
  return request({
    url: '/api/sensors/history',
    method: 'get'
  })
} 