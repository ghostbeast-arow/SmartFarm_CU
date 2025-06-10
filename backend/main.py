"""
MQTT数据模拟程序
"""
import time
from mqtt_client import MQTTClient

def main():
    try:
        # 初始化MQTT客户端（负责发送模拟数据）
        mqtt_client = MQTTClient()
        
        # 启动数据模拟
        mqtt_client.start_simulation()
        
        print("MQTT数据模拟程序已启动，正在发送模拟数据...")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在关闭MQTT数据模拟程序...")
        if 'mqtt_client' in locals():
            mqtt_client.cleanup()
    except Exception as e:
        print(f"程序运行出错: {e}")
        if 'mqtt_client' in locals():
            mqtt_client.cleanup()

if __name__ == '__main__':
    main()