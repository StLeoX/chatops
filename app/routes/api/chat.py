import logging

from flask import Blueprint, request, abort
from flask_login import current_user

import app
from app.utils.api import success_response, error_response
from app import the_redis as redis

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/gpt_ping", methods=["GET"])
def gpt_ping():
    """
    检查 GPT 服务的可用性
    ---

    parameters: []

    responses:
      503:
        description: GPT 服务不可用
        schema:
          properties:
            error:
              type: string
              description: 错误信息说明服务不可用
      200:
        description: GPT 服务可用
        schema:
          properties:
            response:
              type: boolean
              description: 表示GPT服务是否可用

    """

    succ = app.the_chat_manager.gpt_ping()
    if not succ:
        return error_response("GPT 不可用，请检查")

    return success_response("GPT 暂时可用")


@chat_bp.route("/gpt_update_key", methods=["POST"])
def gpt_update_key():
    """
    更新GPT的API密钥
    ---

    parameters:
      - name: key
        description: 新的API密钥
        in: body
        type: string
        required: true

    responses:
      400:
        description: 请求有误
      401:
        description: 密钥错误
        schema:
          properties:
            error:
              type: string
              description: 错误信息说明密钥无效
      200:
        description: 密钥更新成功
        schema:
          properties:
            response:
              type: boolean
              description: 表示密钥是否成功更新

    """

    key = request.json["key"]
    if not key:
        return error_response("key not in request", 400)

    succ = app.the_chat_manager.gpt_update_key(key)
    if not succ:
        return error_response("更新秘钥失败", 503)

    return success_response("echo key " + key)


@chat_bp.route("/gpt_stop", methods=["GET"])
def gpt_stop():
    """
    停止GPT服务的当前操作
    ---

    parameters: []

    responses:
      200:
        description: 操作成功停止
        schema:
          properties:
            response:
              type: boolean
              description: 表示操作是否已成功停止

    """

    # TODO: stop generation
    return error_response("未实现")


@chat_bp.route("/gen_fault_desc", methods=["POST"])
def gen_fault_desc():
    """
    故障场景描述
    ---

    parameters:
      - name: fault
        description: 故障 JSON
        in: body
        type: object
        required: true
        schema:
          properties:
            workflowInfo:
              type: object
              description: 工作流配置
            faultConfigInfo:
              type: object
              description: 故障配置

    responses:
      400:
        description: 请求有误
      401:
        description: 未登录
      503:
        description: 生成失败
      200:
        description: 生成成功
        schema:
          properties:
            fault_desc:
              type: string
              description: 故障描述

    """

    if not current_user:
        return error_response("请先登录", 401)

    fault_workflow = request.json["workflowInfo"]
    if not fault_workflow:
        return error_response("fault_workflow not in request", 400)

    fault_config = request.json["faultConfigInfo"]
    if not fault_config:
        return error_response("fault_config not in request", 400)

    fid, fault_desc = app.the_chat_manager.gen_fault_desc(fault_workflow, fault_config)

    if not fid:
        return error_response("生成故障场景描述失败", 503)

    logging.debug(f"response fault {fid}")
    return success_response({"fault_desc": fault_desc})


@chat_bp.route("/gen_fault_result", methods=["POST"])
def gen_fault_result():
    """
    故障结果，包含以下三个方面：
    - 演练结果
    - 问题分析
    - 运维建议
    ---

    parameters:
      - name: fault
        description: 故障结果 JSON
        in: body
        type: object
        required: true
        schema:
          properties:
            fid:
              type: integer
              description: 故障 ID
            faultPlayInfo:
              type: object
              description: 故障结果

    responses:
      400:
        description: 请求有误
      401:
        description: 未登录
      503:
        description: 生成失败
      200:
        description: 生成成功
        schema:
          properties:
            report:
              type: string
              description: 故障演练结果
            analysis:
              type: string
              description: 故障问题分析
            advice:
              type: string
              description: 运维建议

    """

    if not current_user:
        return error_response("请先登录", 401)

    fid = request.json["fid"]
    if not fid:
        return error_response("fid not in request", 400)
    fid = int(fid)

    fault_play = {"faultPlayInfo": request.json["faultPlayInfo"]}
    if not fault_play:
        return error_response("fault_play not in request", 400)

    rid, report, analysis = app.the_chat_manager.gen_fault_result(fid, fault_play)
    if not rid:
        logging.warning(f"not gen report {rid}")
        return error_response("生成故障报告失败", 503)
    logging.debug(f"response report {rid}")

    aid, advice = app.the_chat_manager.gen_advice(fid)
    if not aid:
        logging.warning(f"not gen advice {aid}")
        return error_response("生成运维建议失败", 503)
    logging.debug(f"response advice {aid}")

    return success_response({"report": report,
                             "analysis": analysis,
                             "advice": advice})


@chat_bp.route("/gen_expect", methods=["POST"])
def gen_expect():
    """
    用户期望描述
    ---

    todo
    """

    if not current_user:
        return error_response("请先登录", 401)

    fid = request.json["fid"]
    if not fid:
        return error_response("fid not in request", 400)
    fid = int(fid)

    fault = redis.hget('faults', fid).decode()
    if not fault:
        logging.error("fault no found")
        return error_response("故障不存在", 404)

    expectation_text = request.json["expect"]
    if not expectation_text:
        return error_response("expectation_text not in request", 400)

    eid, expectation = app.the_chat_manager.gen_expect(expectation_text)
    if not eid:
        return error_response("生成用户期望 JSON 失败", 503)

    logging.debug(f"response expectation {eid}")
    # todo: 针对返回 json 需要特殊处理下？
    return success_response(expectation)
