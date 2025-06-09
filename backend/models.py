from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Crop(db.Model):
    """作物类型模型"""
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # 作物名称
    
    # 温度阈值
    temp_day_limit = db.Column(db.String(50), nullable=False)  # 格式: "min,max"
    temp_night_limit = db.Column(db.String(50), nullable=False)  # 格式: "min,max"
    
    # 湿度阈值
    humidity_day_limit = db.Column(db.String(50), nullable=False)
    humidity_night_limit = db.Column(db.String(50), nullable=False)
    
    # 光照阈值
    light_day_limit = db.Column(db.String(50), nullable=False)
    light_night_limit = db.Column(db.String(50), nullable=False)
    
    # 土壤pH阈值
    soil_day_limit = db.Column(db.String(50), nullable=False)
    soil_night_limit = db.Column(db.String(50), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_thresholds(self):
        """获取阈值数据"""
        def parse_limit(limit_str):
            min_val, max_val = map(float, limit_str.split(','))
            return {'min': min_val, 'max': max_val}
            
        return {
            'temperature': {
                'day': parse_limit(self.temp_day_limit),
                'night': parse_limit(self.temp_night_limit)
            },
            'humidity': {
                'day': parse_limit(self.humidity_day_limit),
                'night': parse_limit(self.humidity_night_limit)
            },
            'light': {
                'day': parse_limit(self.light_day_limit),
                'night': parse_limit(self.light_night_limit)
            },
            'soil': {
                'day': parse_limit(self.soil_day_limit),
                'night': parse_limit(self.soil_night_limit)
            }
        } 