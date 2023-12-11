import logging

from flask import Blueprint, request, abort
from flask_login import current_user

import app
from app.utils.api import success_response, error_response
from app.extensions.db import db as redis

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/gpt_ping", methods=["GET"])
def gpt_ping():
    """
    返回 GPT 可用性
    void
    boolean
    """

    # todo(xla)
    # the_gpt.Ping()
    return success_response("ping " + str(True))


@chat_bp.route("/gpt_update_key", methods=["POST"])
def gpt_update_key():
    """
    更新GPT apikey
    string
    boolean
    """

    # todo(xla)
    key = request.json["key"]
    return success_response("echo key " + key)


@chat_bp.route("/gpt_stop", methods=["GET"])
def gpt_stop():
    """
    停止生成
    void
    boolean
    """

    # todo(xla)
    return success_response("stop " + str(True))


@chat_bp.route("/gen_fault_desc", methods=["POST"])
def gen_fault_desc():
    """
    故障场景描述
    fault json
    boolean, string
    """

    fault_data = request.json["fault"]
    fault_id = fault_data["fid"]
    return success_response("fault_id " + fault_id)


@chat_bp.route("/gen_expect", methods=["POST"])
def gen_expect():
    """
    用户期望描述
    fault_id
    expectation json
    """

    # todo(xla)
    fault_id = request.json["fid"]
    return success_response("expect nothing")


@chat_bp.route("/gen_fault_report", methods=["POST"])
def gen_fault_report():
    """
    故障结果描述
    fault_id
    boolean, string
    """

    if not current_user:
        return error_response("请先登录", 401)

    fid = request.json["fid"]
    fault = redis.hget('faults', fid)
    if not fault:
        logging.error("fault no found")
        return error_response("故障不存在", 404)

    rid, report = app.the_chat_manager.gen_fault_report(fid)
    if not rid:
        return error_response("生成故障报告失败")

    logging.debug(f"response report {rid}")
    return success_response(report)


@chat_bp.route("/gen_advice", methods=["POST"])
def gen_advice():
    """
    生成运维建议
    fault_id
    boolean, string
    """

    if not current_user:
        return error_response("请先登录", 401)

    fid = request.json["fid"]
    fault = redis.hget('faults', fid)
    if not fault:
        logging.error("fault no found")
        return error_response("故障不存在", 404)

    aid, advice = app.the_chat_manager.gen_advice(fid)
    if not aid:
        return error_response("生成运维建议失败")

    logging.debug(f"response advice {aid}")
    return success_response(advice)
