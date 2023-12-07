from functools import wraps
from flask import request, jsonify


def validate_json_length(json_obj, max_length):
    # 验证JSON对象的长度是否超过最大限制
    return len(json_obj) <= max_length

def validate_name(name):
    # 验证用户名是否合法
    return len(name) >= 3 and len(name) <= 32

def validate_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        username = data.get('name')
        api_key = data.get('api_key')

        if validate_json_length(data, 256) is False:
            return jsonify({'error': 'JSON对象长度不合法'}), 400
        if not username:
            return jsonify({'error': '用户名不能为空'}), 400
        if not api_key:
            return jsonify({'error': 'api_key 不能为空'}), 400
        if not validate_name(username):
            return jsonify({'error': '用户名长度不合法'}), 400

        if not api_key.startswith('sk-'):
            return jsonify({'error': 'api_key 需要以 "sk-" 开头'}), 400

        return f(*args, **kwargs)

    return decorated_function

def mock_validate_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Mock login validation performed")
        return f(*args, **kwargs)
    return decorated_function

def validate_logout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        username = data.get('name')

        if validate_json_length(data, 256) is False:
            return jsonify({'error': 'JSON对象长度不合法'}), 400
        if not username:
            return jsonify({'error': '用户名不能为空'}), 400
        if not validate_name(username):
            return jsonify({'error': '用户名长度不合法'}), 400

        return f(*args, **kwargs)
    
    return decorated_function