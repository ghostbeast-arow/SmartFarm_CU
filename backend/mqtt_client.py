"""
MQTT客户端模块
"""
import paho.mqtt.client as mqtt
import json
import random
import time
import threading
from datetime import datetime
from config import MQTT_CONFIG, SENSOR_CONFIG, SIMULATION_INTERVAL

class MQTTClient:
    def __init__(self):
        """初始化MQTT客户端"""
        self.client = None
        self.simulation_running = False
        self.simulation_thread = None
        self._setup_client()

    def _setup_client(self):
        """设置MQTT客户端"""
        try:
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()

            self.client = mqtt.Client(MQTT_CONFIG['client_id'] + '_simulator')
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            
            # 设置认证信息
            self.client.username_pw_set(MQTT_CONFIG['username'], MQTT_CONFIG['password'])
            
            # 连接到MQTT代理
            self.client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], 60)
            self.client.loop_start()
            print("MQTT客户端已连接到代理")
        except Exception as e:
            print(f"设置MQTT客户端时出错: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc):
        """连接回调"""
        if rc == 0:
            print("MQTT客户端成功连接到代理")
        else:
            print(f"MQTT连接失败，返回码: {rc}")

    def on_disconnect(self, client, userdata, rc):
        """断开连接回调"""
        if rc != 0:
            print("MQTT意外断开连接")
            # 尝试重新连接
            self._setup_client()
        else:
            print("MQTT已断开连接")

    def publish_data(self, topic, data):
        """发布数据到MQTT主题"""
        try:
            if not self.client or not self.client.is_connected():
                self._setup_client()

            # 确保数据是JSON字符串
            if isinstance(data, dict):
                data = json.dumps(data)
            elif not isinstance(data, str):
                data = str(data)
            
            # 发布消息
            result = self.client.publish(topic, data)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"已发布数据到主题 {topic}: {data}")
            else:
                print(f"发布数据失败，错误码: {result.rc}")
        except Exception as e:
            print(f"发布数据时出错: {e}")

    def start_simulation(self):
        """开始模拟数据发送"""
        if self.simulation_running:
            return

        def simulation_loop():
            self.simulation_running = True
            while self.simulation_running:
                try:
                    # 生成符合范围的传感器数据
                    sensor_data = self._generate_sensor_data()
                    
                    # 遍历所有传感器类型
                    for i, data_type in enumerate(SENSOR_CONFIG['data_types'], 1):
                        # 准备数据
                        data = {
                            'sensor_id': i,
                            'data_type': data_type,
                            'value': sensor_data[data_type.lower()],
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # 发布数据
                        self.publish_data(f"sensors/{i}/data", data)
                    
                    # 等待一段时间后再次发送
                    time.sleep(SIMULATION_INTERVAL)
                    
                except Exception as e:
                    print(f"模拟数据发送出错: {e}")
                    time.sleep(5)  # 出错后等待一段时间再重试

        # 启动模拟线程
        self.simulation_thread = threading.Thread(target=simulation_loop)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        print("开始模拟数据发送...")

    def cleanup(self):
        """清理资源"""
        try:
            # 停止模拟
            self.simulation_running = False
            if self.simulation_thread:
                self.simulation_thread.join(timeout=1)
            
            # 断开MQTT连接
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()
            
            print("MQTT客户端已清理")
        except Exception as e:
            print(f"清理MQTT客户端时出错: {e}")

    def _generate_sensor_data(self):
        """生成模拟的传感器数据"""
        return {
            'temperature': round(random.uniform(20, 30), 1),  # 温度范围20-30℃
            'humidity': round(random.uniform(50, 90), 1),     # 湿度范围40-60%
            'soil': round(random.uniform(6.0, 7.5), 1),  # 土壤pH范围6.0-7.5，适合大多数植物生长
            'light': round(random.uniform(1000, 5000), 1)    # 光照范围1000-5000lux
        } 