<template>
  <el-dialog
    v-model="dialogVisible"
    title="Crop Type Management"
    width="80%"
    :before-close="handleClose"
  >
    <div class="crop-settings">
      <!-- Crop Type Tabs -->
      <div class="crop-tabs">
        <div class="tabs-container">
          <div
            v-for="crop in crops"
            :key="crop.id"
            class="tab-item"
            :class="{ active: selectedCrop?.id === crop.id }"
            @click="selectCrop(crop)"
          >
            <span>{{ crop.name }}</span>
            <el-tooltip content="Delete this crop type" placement="top">
              <el-icon class="delete-icon" @click.stop="handleDelete(crop)">
                <Close />
              </el-icon>
            </el-tooltip>
          </div>
          <el-tooltip content="Add new crop type" placement="top">
            <div class="add-tab" @click="handleAdd">
              <el-icon><Plus /></el-icon>
            </div>
          </el-tooltip>
        </div>
      </div>

      <!-- Crop Settings Form -->
      <div v-if="selectedCrop" class="crop-form">
        <el-form :model="form" label-width="120px">
          <el-form-item label="Crop Name">
            <el-input v-model="form.name" placeholder="Enter crop name" />
          </el-form-item>
          
          <!-- Temperature Settings -->
          <div class="threshold-section">
            <h3>Temperature Thresholds (°C)</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Day Min">
                  <el-input-number v-model="form.thresholds.temperature.day.min" :min="0" :max="50" />
                </el-form-item>
                <el-form-item label="Day Max">
                  <el-input-number v-model="form.thresholds.temperature.day.max" :min="0" :max="50" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Night Min">
                  <el-input-number v-model="form.thresholds.temperature.night.min" :min="0" :max="50" />
                </el-form-item>
                <el-form-item label="Night Max">
                  <el-input-number v-model="form.thresholds.temperature.night.max" :min="0" :max="50" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Humidity Settings -->
          <div class="threshold-section">
            <h3>Humidity Thresholds (%)</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Day Min">
                  <el-input-number v-model="form.thresholds.humidity.day.min" :min="0" :max="100" />
                </el-form-item>
                <el-form-item label="Day Max">
                  <el-input-number v-model="form.thresholds.humidity.day.max" :min="0" :max="100" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Night Min">
                  <el-input-number v-model="form.thresholds.humidity.night.min" :min="0" :max="100" />
                </el-form-item>
                <el-form-item label="Night Max">
                  <el-input-number v-model="form.thresholds.humidity.night.max" :min="0" :max="100" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Light Settings -->
          <div class="threshold-section">
            <h3>Light Thresholds (lux)</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Day Min">
                  <el-input-number v-model="form.thresholds.light.day.min" :min="0" :max="10000" />
                </el-form-item>
                <el-form-item label="Day Max">
                  <el-input-number v-model="form.thresholds.light.day.max" :min="0" :max="10000" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Night Min">
                  <el-input-number v-model="form.thresholds.light.night.min" :min="0" :max="10000" />
                </el-form-item>
                <el-form-item label="Night Max">
                  <el-input-number v-model="form.thresholds.light.night.max" :min="0" :max="10000" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <!-- Soil pH Settings -->
          <div class="threshold-section">
            <h3>Soil pH Thresholds</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Day Min">
                  <el-input-number v-model="form.thresholds.soil.day.min" :min="0" :max="14" :precision="1" />
                </el-form-item>
                <el-form-item label="Day Max">
                  <el-input-number v-model="form.thresholds.soil.day.max" :min="0" :max="14" :precision="1" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Night Min">
                  <el-input-number v-model="form.thresholds.soil.night.min" :min="0" :max="14" :precision="1" />
                </el-form-item>
                <el-form-item label="Night Max">
                  <el-input-number v-model="form.thresholds.soil.night.max" :min="0" :max="14" :precision="1" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </el-form>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary" @click="handleSave">Save</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Close, Plus } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'refresh'])

const dialogVisible = ref(props.modelValue)
const crops = ref([])
const selectedCrop = ref(null)

// 监听对话框显示状态
watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
  if (val) {
    fetchCrops()
  }
})

watch(dialogVisible, (val) => {
  emit('update:modelValue', val)
})

// 表单数据
const form = reactive({
  name: '',
  thresholds: {
    temperature: {
      day: { min: 20, max: 30 },
      night: { min: 15, max: 25 }
    },
    humidity: {
      day: { min: 40, max: 70 },
      night: { min: 50, max: 80 }
    },
    light: {
      day: { min: 1000, max: 5000 },
      night: { min: 0, max: 100 }
    },
    soil: {
      day: { min: 5.5, max: 7.0 },
      night: { min: 5.5, max: 7.0 }
    }
  }
})

// 获取所有作物类型
const fetchCrops = async () => {
  try {
    const response = await fetch('/api/crops')
    const data = await response.json()
    crops.value = data
    if (data.length > 0) {
      selectCrop(data[0])
    }
  } catch (error) {
    ElMessage.error('Failed to fetch crop types')
  }
}

// 选择作物
const selectCrop = (crop) => {
  selectedCrop.value = crop
  form.name = crop.name
  form.thresholds = crop.thresholds
}

// 添加新作物
const handleAdd = () => {
  selectedCrop.value = null
  form.name = ''
  form.thresholds = {
    temperature: {
      day: { min: 20, max: 30 },
      night: { min: 15, max: 25 }
    },
    humidity: {
      day: { min: 40, max: 70 },
      night: { min: 50, max: 80 }
    },
    light: {
      day: { min: 1000, max: 5000 },
      night: { min: 0, max: 100 }
    },
    soil: {
      day: { min: 5.5, max: 7.0 },
      night: { min: 5.5, max: 7.0 }
    }
  }
}

// 删除作物
const handleDelete = async (crop) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete crop "${crop.name}"?`,
      'Warning',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    const response = await fetch(`/api/crops/${crop.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('Successfully deleted')
      await fetchCrops()
      emit('refresh')
    } else {
      ElMessage.error('Failed to delete')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete')
    }
  }
}

// 保存作物设置
const handleSave = async () => {
  try {
    if (!form.name.trim()) {
      ElMessage.warning('Please enter crop name')
      return
    }

    const method = selectedCrop.value ? 'PUT' : 'POST'
    const url = selectedCrop.value ? `/api/crops/${selectedCrop.value.id}` : '/api/crops'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: form.name,
        thresholds: form.thresholds
      })
    })
    
    if (response.ok) {
      ElMessage.success(selectedCrop.value ? 'Successfully updated' : 'Successfully added')
      await fetchCrops()
      emit('refresh')
    } else {
      const data = await response.json()
      ElMessage.error(data.error || 'Failed to save')
    }
  } catch (error) {
    ElMessage.error('Failed to save')
  }
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
}
</script>

<style scoped>
.crop-settings {
  height: 60vh;
  display: flex;
  flex-direction: column;
}

.crop-tabs {
  border-bottom: 1px solid #dcdfe6;
  margin-bottom: 20px;
}

.tabs-container {
  display: flex;
  align-items: center;
  overflow-x: auto;
  padding-bottom: 10px;
}

.tab-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  margin-right: 4px;
  border: 1px solid #dcdfe6;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-item:hover {
  background-color: #ecf5ff;
}

.tab-item.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.delete-icon {
  margin-left: 8px;
  font-size: 14px;
  opacity: 0.7;
}

.delete-icon:hover {
  opacity: 1;
}

.add-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.add-tab:hover {
  border-color: #409eff;
  color: #409eff;
}

.crop-form {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.threshold-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.threshold-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #606266;
  font-size: 16px;
}

:deep(.el-form-item) {
  margin-bottom: 15px;
}
</style> 