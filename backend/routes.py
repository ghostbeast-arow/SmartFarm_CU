from flask import Blueprint, jsonify, request
from models import db, Crop

# 创建蓝图
bp = Blueprint('api', __name__)

# 作物管理相关路由
@bp.route('/crops', methods=['GET'])
def get_crops():
    """获取所有作物信息"""
    try:
        crops = Crop.query.all()
        print(f"Found {len(crops)} crops in database")
        
        result = []
        for crop in crops:
            try:
                crop_data = {
                    'id': crop.id,
                    'name': crop.name,
                    'thresholds': crop.get_thresholds()
                }
                result.append(crop_data)
                print(f"Successfully processed crop: {crop.name}")
            except Exception as e:
                print(f"Error processing crop {crop.name}: {str(e)}")
                continue
                
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in get_crops: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/crops', methods=['POST'])
def create_crop():
    """创建新作物类型"""
    data = request.json
    
    # 检查作物名称是否已存在
    if Crop.query.filter_by(name=data['name']).first():
        return jsonify({'error': '作物名称已存在'}), 400
        
    # 将阈值转换为字符串格式
    def format_limit(threshold):
        return f"{threshold['min']},{threshold['max']}"
        
    crop = Crop(
        name=data['name'],
        temp_day_limit=format_limit(data['thresholds']['temperature']['day']),
        temp_night_limit=format_limit(data['thresholds']['temperature']['night']),
        humidity_day_limit=format_limit(data['thresholds']['humidity']['day']),
        humidity_night_limit=format_limit(data['thresholds']['humidity']['night']),
        light_day_limit=format_limit(data['thresholds']['light']['day']),
        light_night_limit=format_limit(data['thresholds']['light']['night']),
        soil_day_limit=format_limit(data['thresholds']['soil']['day']),
        soil_night_limit=format_limit(data['thresholds']['soil']['night'])
    )
    
    db.session.add(crop)
    db.session.commit()
    
    return jsonify({'message': '作物添加成功', 'id': crop.id}), 201

@bp.route('/api/crops/<int:crop_id>', methods=['PUT'])
def update_crop(crop_id):
    """更新作物类型"""
    crop = Crop.query.get_or_404(crop_id)
    data = request.json
    
    # 检查新名称是否与其他作物重复
    if data['name'] != crop.name and Crop.query.filter_by(name=data['name']).first():
        return jsonify({'error': '作物名称已存在'}), 400
        
    # 将阈值转换为字符串格式
    def format_limit(threshold):
        return f"{threshold['min']},{threshold['max']}"
        
    crop.name = data['name']
    crop.temp_day_limit = format_limit(data['thresholds']['temperature']['day'])
    crop.temp_night_limit = format_limit(data['thresholds']['temperature']['night'])
    crop.humidity_day_limit = format_limit(data['thresholds']['humidity']['day'])
    crop.humidity_night_limit = format_limit(data['thresholds']['humidity']['night'])
    crop.light_day_limit = format_limit(data['thresholds']['light']['day'])
    crop.light_night_limit = format_limit(data['thresholds']['light']['night'])
    crop.soil_day_limit = format_limit(data['thresholds']['soil']['day'])
    crop.soil_night_limit = format_limit(data['thresholds']['soil']['night'])
    
    db.session.commit()
    return jsonify({'message': '作物更新成功'})

@bp.route('/api/crops/<int:crop_id>', methods=['DELETE'])
def delete_crop(crop_id):
    """删除作物类型"""
    crop = Crop.query.get_or_404(crop_id)
    db.session.delete(crop)
    db.session.commit()
    return jsonify({'message': '作物删除成功'}) 