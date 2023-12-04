# Flask modules
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from flask_login import login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask import request, jsonify

# Other modules
import logging

# Local modules
from app.models.auth import User
from app.extensions import db, bcrypt

from app.utils.auth import validate_api_key


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.before_request
def before_request():
    print("Incoming request:", request.url, request.method, request.json)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    if not data.get('name'):
        return jsonify({"message": "用户名不能为空"}), 400
    
    if not validate_api_key(data.get('apt_key')):
        return jsonify({"message": "API key 不合法"}), 401

    try:
        user = User(data.get('name'), data.get('api_key'))
    except ValueError as e:
        print(str(e)) # Username already exists
        return jsonify({"message": "用户名已存在"}), 409
    
    login_user(user)
    
    return jsonify({"message": "登录成功"}), 200


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    data = request.json
    current_user = User()
    current_user.load(data.get('name'))
    if not current_user.is_authenticated:
        # 处理未登录的情况，例如返回特定的响应
        return jsonify({"message": "未登录"}), 401

    logout_user()
    current_user.delete()
    return jsonify({"message": "用户已注销"})