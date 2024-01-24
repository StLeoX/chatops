# Flask modules
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from flask_login import login_user, logout_user

from flask import request, jsonify

# Other modules
import logging

# Local modules
import app
from app.models.auth import User

from app.utils.auth import validate_login, validate_logout
from app.utils.api import success_response, error_response
from app.prompt.gpt_chat_manager import GptChatManager

auth_bp = Blueprint("auth", __name__, url_prefix="/v1")


@auth_bp.before_request
def before_request():
    logging.info("Incoming request:", request.url, request.method, request.json)


@auth_bp.route('/login', methods=['POST'])
@validate_login
def login():
    data = request.json
    logging.debug(data)

    try:
        user = User(data.get('name'), data.get('api_key'))
    except ValueError as e:
        logging.info(str(e))
        return error_response("用户名已存在", 409)

    login_user(user)

    # 初始化 chat
    app.the_chat_manager = GptChatManager()
    if not app.the_chat_manager.gpt_ping():
        return error_response("GPT 不可用")

    return success_response("登录成功")


@auth_bp.route("/logout", methods=["GET", "POST"])
@validate_logout
def logout():
    data = request.json
    current_user = User()
    current_user.load(data.get('name'))
    if not current_user.is_authenticated:
        # 处理未登录的情况，返回401
        return jsonify({"message": "未登录"}), 401

    logout_user()
    # 从数据库中删除用户
    current_user.delete()
    return jsonify({"message": "用户已注销"})
