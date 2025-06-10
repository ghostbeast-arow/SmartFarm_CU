# 智能农场监控系统

基于 Vue 3 + Flask + MQTT 的智能农场监控系统，用于实时监控和管理农场传感器数据。

## 系统要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- MQTT Broker (如 Mosquitto)

## 后端设置

1. 安装 Python 依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 配置数据库：
- 在 MySQL 中创建数据库
- 修改 `backend/config.py` 中的数据库配置：
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'port': 3306
}
```

3. 启动后端服务：
```bash
python backend/app.py
```

## 前端设置

1. 安装 Node.js 依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm run serve
```

## 系统功能

- 实时监控传感器数据
- 传感器状态管理
- 告警信息管理
- 数据可视化展示

## 技术栈

- 前端：Vue 3 + Element Plus
- 后端：Flask + MySQL
- 通信：MQTT
- 数据库：MySQL

## 目录结构

```
├── backend/                # 后端代码
│   ├── app.py             # Flask 应用入口
│   ├── config.py          # 配置文件
│   ├── db_manager.py      # 数据库管理
│   └── mqtt_client.py     # MQTT 客户端
└── frontend/              # 前端代码
    ├── src/               # 源代码
    ├── public/            # 静态资源
    └── package.json       # 项目配置
```

## 功能特性

### 1. 实时数据监控
- 温度趋势实时图表
- 环境参数分布展示
- 传感器状态监控
- 实时告警信息推送

### 2. 历史数据查询
- 支持按天数查询（1天、3天、7天、14天、30天）
- 数据统计概览（平均值、最大值、最小值）
- 历史数据趋势图
- 详细数据表格展示

## 使用说明

### 1. 访问系统
- 后端API服务：`http://localhost:5000`
- 前端界面：`http://localhost:5173`

### 2. 实时监控
- 在仪表盘页面查看实时数据
- 选择不同传感器查看温度趋势
- 查看环境参数分布和传感器状态
- 监控实时告警信息

### 3. 历史数据查询
- 选择要查询的传感器
- 选择数据类型（温度、湿度等）
- 选择查询天数
- 查看数据统计和趋势图
- 在表格中查看详细数据

## 项目结构

```
├── __pycache__/           # Python缓存文件
├── .idea/                 # IDE配置文件
├── frontend/             # 前端Vue应用
├── mqtt_client/          # MQTT客户端模块
│   ├── mqtt_client.py    # MQTT客户端实现
├── app.py               # Flask API服务
├── config.py            # 系统配置文件
├── db_manager.py        # 数据库管理模块
├── main.py              # 主程序入口
├── README.md            # 项目说明文档
└── requirements.txt     # Python依赖配置
```

### 核心文件说明

1. `main.py`
   - 系统主程序入口
   - 初始化和启动MQTT客户端
   - 处理系统信号和优雅退出

2. `app.py`
   - Flask API服务实现
   - 提供传感器数据查询接口
   - 提供历史数据统计接口
   - 提供告警信息查询接口
   - 集成MQTT客户端和数据库操作

3. `config.py`
   - 数据库配置
   - MQTT代理配置
   - 传感器配置
   - 系统参数配置

4. `db_manager.py`
   - 数据库管理类
   - 数据库初始化
   - 数据表创建
   - 数据库操作接口

5. `mqtt_client/mqtt_client.py`
   - MQTT客户端实现
   - 传感器数据采集
   - 数据发布订阅
   - 连接管理

## 配置说明

### 1. 数据库配置
在 `database/db_manager.py` 中配置数据库连接信息：
```python
DB_PATH = 'database/smart_farm.db'
```

### 2. MQTT配置
在 `mqtt_client/mqtt_client.py` 中配置MQTT连接信息：
```python
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_USERNAME = 'your_username'
MQTT_PASSWORD = 'your_password'
```

### 3. API配置
在 `api/config.py` 中配置API服务信息：
```python
API_HOST = '0.0.0.0'
API_PORT = 5000
```

## 开发说明

### 1. 添加新的传感器
1. 在 `mqtt_client/sensor_simulator.py` 中添加新的传感器类型
2. 在数据库中添加相应的表结构
3. 在前端添加对应的数据展示组件

### 2. 添加新的数据展示
1. 在 `frontend/src/components` 中创建新的组件
2. 在 `frontend/src/views/Dashboard.vue` 中集成新组件
3. 在 `frontend/src/api` 中添加相应的API调用

## 注意事项

1. 确保MQTT服务器正常运行
2. 检查数据库连接是否正常
3. 确保所有依赖包都已正确安装
4. 注意API接口的跨域配置

## 许可证

MIT License 