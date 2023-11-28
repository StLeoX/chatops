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


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.before_request
def before_request():
    print("Incoming request:", request.url, request.method, request.json)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    user = User.query.filter_by(email=data.get('email')).first()

    if user and check_password_hash(user.password, data.get('password')):
        login_user(user)
        return jsonify({"message": "登录成功"})
    else:
        return jsonify({"message": "无效的邮箱或密码"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        return jsonify({"message": "邮箱已被注册"}), 409

    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=generate_password_hash(data.get('password')),
        created_date=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "注册成功"})

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "用户已注销"})