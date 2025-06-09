"""
配置文件
"""

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',  # 替换为你的 MySQL 用户名
    'password': 'Zby_280304',  # 替换为你的 MySQL 密码
    'database': 'smart_farm'  # 数据库名称
}

# MQTT配置
MQTT_CONFIG = {
    'broker': 'localhost',
    'port': 1883,
    'username': '',  # MQTT broker的用户名
    'password': '',  # MQTT broker的密码
    'topic_prefix': 'greenhouse/',
    'client_id': 'greenhouse_server'
}

# 登录配置
LOGIN_CONFIG = {
    'username': 'admin',
    'password': 'admin123'
}

# 传感器配置
SENSOR_CONFIG = {
    'total_sensors': 4,
    'data_types': ['temperature', 'humidity', 'soil', 'light'],
    'ranges': {
        'temperature': (20, 30),
        'humidity': (50, 90),
        'light': (800, 1200),
        'soil': (30, 50)
    },
    'units': {
        'temperature': '°C',
        'humidity': '%',
        'light': 'lux',
        'soil': 'pH'
    }
}

# 数据采集间隔（秒）
COLLECTION_INTERVAL = 30
# 数据模拟间隔（秒）
SIMULATION_INTERVAL = 30