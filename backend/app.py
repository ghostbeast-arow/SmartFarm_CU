"""
API服务入口
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from db_manager import DatabaseManager
from config import DB_CONFIG, MQTT_CONFIG, SENSOR_CONFIG, LOGIN_CONFIG
from models import db, Crop
from routes import bp

def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置CORS
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
    
    # 初始化扩展
    db.init_app(app)
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    # 初始化数据库
    if not db_manager.init_database(app, db):
        print("警告：数据库初始化失败")
    else:
        print("数据库初始化成功")
    
    # 注册蓝图
    app.register_blueprint(bp, url_prefix='/api')
    
    return app, db_manager

# 创建应用实例和数据库管理器
app, db_manager = create_app()

# 创建默认作物数据
def create_default_crops():
    """创建默认作物数据"""
    from models import Crop
    
    default_crops = [
        {
            'name': 'Tomato',
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
            'name': 'Potato',
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
                print(f"Added default crop: {crop_data['name']}")
        except Exception as e:
            print(f"Error adding default crop {crop_data['name']}: {str(e)}")
            continue
    
    try:
        db.session.commit()
        print("Successfully added default crops")
    except Exception as e:
        print(f"Error committing default crops: {str(e)}")
        db.session.rollback()

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """获取所有传感器信息"""
    try:
        sensors = db_manager.get_all_sensors()
        return jsonify({
            'success': True,
            'data': sensors
        })
    except Exception as e:
        print(f"获取传感器信息失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/history', methods=['GET'])
def get_sensor_history():
    """获取传感器历史数据"""
    try:
        # 获取查询参数
        limit = request.args.get('limit', default=100, type=int)
        
        # 从数据库获取历史数据
        history_data = db_manager.get_sensor_history(limit)
        
        # 按传感器类型组织数据
        formatted_data = {
            'temperature': [],
            'humidity': [],
            'light': [],
            'soil_moisture': []
        }
        
        # 格式化数据
        for record in history_data:
            sensor_type = record['data_type'].lower()
            if sensor_type in formatted_data:
                formatted_data[sensor_type].append({
                    'time': record['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'value': float(record['value'])
                })
        
        return jsonify({
            'success': True,
            'data': formatted_data
        })
    except Exception as e:
        print(f"获取历史数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """获取单个传感器信息"""
    try:
        sensor = db_manager.get_sensor_by_id(sensor_id)
        if sensor:
            return jsonify({
                'success': True,
                'data': sensor
            })
        else:
            return jsonify({
                'success': False,
                'error': '传感器不存在'
            }), 404
    except Exception as e:
        print(f"获取传感器信息失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors', methods=['POST'])
def add_sensor():
    """添加新传感器"""
    try:
        data = request.get_json()
        # 实现添加传感器的逻辑
        return jsonify({
            'success': True,
            'message': '传感器添加成功'
        })
    except Exception as e:
        print(f"添加传感器失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    """更新传感器信息"""
    try:
        data = request.get_json()
        # 实现更新传感器的逻辑
        return jsonify({
            'success': True,
            'message': '传感器更新成功'
        })
    except Exception as e:
        print(f"更新传感器失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    """删除传感器"""
    try:
        # 实现删除传感器的逻辑
        return jsonify({
            'success': True,
            'message': '传感器删除成功'
        })
    except Exception as e:
        print(f"删除传感器失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    """获取传感器数据"""
    try:
        data_type = request.args.get('type')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        days = request.args.get('days')
        
        if days:
            days = int(days)
        
        data = db_manager.get_sensor_data(
            sensor_id=sensor_id,
            data_type=data_type,
            start_time=start_time,
            end_time=end_time,
            days=days
        )
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>/latest', methods=['GET'])
def get_latest_sensor_data(sensor_id):
    """获取最新传感器数据"""
    try:
        data = db_manager.get_latest_sensor_data(sensor_id)
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': '没有找到数据'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/stats', methods=['GET'])
def get_sensor_stats():
    """获取传感器统计数据"""
    try:
        stats = db_manager.get_sensor_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """获取告警信息"""
    try:
        alerts = db_manager.get_sensor_alerts()
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sensors/<int:sensor_id>/status', methods=['GET'])
def get_sensor_status(sensor_id):
    """获取传感器状态"""
    try:
        status = db_manager.get_sensor_status(sensor_id)
        if status:
            return jsonify({
                'success': True,
                'data': status
            })
        else:
            return jsonify({
                'success': False,
                'error': '传感器不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    """验证登录密码"""
    try:
        data = request.get_json()
        password = data.get('password')
        
        if password == LOGIN_CONFIG['password']:
            return jsonify({
                'success': True,
                'message': 'Login successful'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    try:
        # 启动Flask应用
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("正在关闭应用...")
        db_manager.cleanup()
    except Exception as e:
        print(f"应用运行出错: {e}")
        db_manager.cleanup() 