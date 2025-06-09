"""
数据库管理器
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import json
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        """初始化数据库管理器"""
        self.connection = None
        self.cursor = None
        self.connect_db()
        self.create_tables()

    def connect_db(self):
        """连接到数据库"""
        try:
            # 使用MySQL的配置
            mysql_config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'Zby_280304',
                'database': 'smart_farm',
                'port': 3306
            }
            self.connection = mysql.connector.connect(**mysql_config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("数据库连接成功")
        except Error as e:
            print(f"连接数据库时出错: {e}")
            raise

    def create_tables(self):
        """创建必要的数据表"""
        try:
            # 创建传感器数据表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_id INT NOT NULL,
                    data_type VARCHAR(50) NOT NULL,
                    value FLOAT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_sensor_timestamp (sensor_id, timestamp)
                )
            """)

            # 创建传感器配置表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    location VARCHAR(100),
                    status VARCHAR(20) DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建告警记录表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_id INT NOT NULL,
                    data_type VARCHAR(50) NOT NULL,
                    value FLOAT NOT NULL,
                    threshold_min FLOAT,
                    threshold_max FLOAT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active',
                    INDEX idx_alert_timestamp (timestamp)
                )
            """)

            self.connection.commit()
            print("数据表创建成功")
        except Error as e:
            print(f"创建数据表时出错: {e}")
            raise

    def insert_sensor_data(self, sensor_id, data_type, value):
        """插入传感器数据"""
        try:
            query = """
                INSERT INTO sensor_data (sensor_id, data_type, value)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (sensor_id, data_type, value))
            self.connection.commit()
        except Error as e:
            print(f"插入传感器数据时出错: {e}")
            self.connection.rollback()

    def get_sensor_data(self, sensor_id=None, data_type=None, start_time=None, end_time=None, days=None):
        """获取传感器数据"""
        try:
            conditions = []
            params = []
            
            if sensor_id:
                conditions.append("sensor_id = %s")
                params.append(sensor_id)
            
            if data_type:
                conditions.append("data_type = %s")
                params.append(data_type)
            
            if days:
                start_time = datetime.now() - timedelta(days=days)
                conditions.append("timestamp >= %s")
                params.append(start_time)
            else:
                if start_time:
                    conditions.append("timestamp >= %s")
                    params.append(start_time)
                if end_time:
                    conditions.append("timestamp <= %s")
                    params.append(end_time)
            
            query = "SELECT * FROM sensor_data"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            query += " ORDER BY timestamp DESC"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取传感器数据时出错: {e}")
            return []

    def get_all_sensors(self):
        """获取所有传感器信息"""
        try:
            self.cursor.execute("SELECT * FROM sensors")
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取传感器信息时出错: {e}")
            return []

    def get_sensor_by_id(self, sensor_id):
        """获取单个传感器信息"""
        try:
            self.cursor.execute("SELECT * FROM sensors WHERE id = %s", (sensor_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"获取传感器信息时出错: {e}")
            return None

    def get_sensor_history(self, limit=100):
        """获取传感器历史数据"""
        try:
            query = """
                SELECT * FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT %s
            """
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取历史数据时出错: {e}")
            return []

    def get_latest_sensor_data(self, sensor_id):
        """获取最新的传感器数据"""
        try:
            query = """
                SELECT * FROM sensor_data
                WHERE sensor_id = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """
            self.cursor.execute(query, (sensor_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"获取最新数据时出错: {e}")
            return None

    def get_sensor_stats(self):
        """获取传感器统计数据"""
        try:
            query = """
                SELECT 
                    data_type,
                    COUNT(*) as total_readings,
                    AVG(value) as avg_value,
                    MIN(value) as min_value,
                    MAX(value) as max_value
                FROM sensor_data
                GROUP BY data_type
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取统计数据时出错: {e}")
            return []

    def get_sensor_alerts(self):
        """获取传感器告警信息"""
        try:
            query = """
                SELECT * FROM alerts
                WHERE status = 'active'
                ORDER BY timestamp DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取告警信息时出错: {e}")
            return []

    def get_sensor_status(self, sensor_id):
        """获取传感器状态"""
        try:
            query = """
                SELECT status FROM sensors
                WHERE id = %s
            """
            self.cursor.execute(query, (sensor_id,))
            result = self.cursor.fetchone()
            return result['status'] if result else None
        except Error as e:
            print(f"获取传感器状态时出错: {e}")
            return None

    def cleanup(self):
        """清理数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                print("数据库连接已关闭")
        except Error as e:
            print(f"清理数据库连接时出错: {e}")

    def __del__(self):
        """析构函数"""
        self.cleanup()

    def init_database(self, app, db):
        """初始化数据库和默认数据"""
        try:
            # 检查数据库是否存在
            check_db_query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{DB_CONFIG['database']}'"
            self.cursor.execute(check_db_query)
            db_exists = self.cursor.fetchone() is not None

            if not db_exists:
                print(f"数据库 {DB_CONFIG['database']} 不存在，正在创建...")
                self.cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
                print(f"数据库 {DB_CONFIG['database']} 创建成功")
            else:
                print(f"数据库 {DB_CONFIG['database']} 已存在")

            # 切换到目标数据库
            self.cursor.execute(f"USE {DB_CONFIG['database']}")

            # 检查必要的表是否存在
            required_tables = ['crops', 'sensor_data', 'sensors', 'alerts']
            existing_tables = []
            
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            for table in tables:
                existing_tables.append(table[list(table.keys())[0]])

            print("现有表:", existing_tables)
            
            with app.app_context():
                # 创建缺失的表
                db.create_all()
                print("所有必要的表已创建或已存在")

                # 检查作物数据是否存在
                from models import Crop
                if 'crops' in existing_tables:
                    crop_count = Crop.query.count()
                    if crop_count == 0:
                        print("作物表为空，添加默认作物数据")
                        self._create_default_crops(db)
                    else:
                        print(f"作物表中已有 {crop_count} 条数据")
                else:
                    print("作物表不存在，创建表并添加默认数据")
                    self._create_default_crops(db)

            print("数据库初始化完成")
            return True
            
        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")
            return False

    def _create_default_crops(self, db):
        """创建默认作物数据"""
        from models import Crop
        
        default_crops = [
            {
                'name': '番茄',
                'temp_day_limit': '20,30',
                'temp_night_limit': '15,25',
                'humidity_day_limit': '60,80',
                'humidity_night_limit': '65,85',
                'light_day_limit': '2000,10000',
                'light_night_limit': '0,100',
                'soil_day_limit': '6.0,7.0',
                'soil_night_limit': '6.0,7.0'
            },
            {
                'name': '黄瓜',
                'temp_day_limit': '22,32',
                'temp_night_limit': '18,28',
                'humidity_day_limit': '65,85',
                'humidity_night_limit': '70,90',
                'light_day_limit': '2500,12000',
                'light_night_limit': '0,100',
                'soil_day_limit': '5.5,7.0',
                'soil_night_limit': '5.5,7.0'
            }
        ]
        
        for crop_data in default_crops:
            try:
                crop = Crop.query.filter_by(name=crop_data['name']).first()
                if not crop:
                    crop = Crop(**crop_data)
                    db.session.add(crop)
                    print(f"添加默认作物: {crop_data['name']}")
            except Exception as e:
                print(f"添加默认作物 {crop_data['name']} 失败: {str(e)}")
                continue
        
        try:
            db.session.commit()
            print("成功添加默认作物数据")
        except Exception as e:
            print(f"提交默认作物数据失败: {str(e)}")
            db.session.rollback() 