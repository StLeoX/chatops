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
      200:
        description: GPT 服务可用
        schema:
          properties:
            response:
              type: boolean
              description: 表示GPT服务是否可用
      503:
        description: GPT 服务不可用
        schema:
          properties:
            error:
              type: string
              description: 错误信息说明服务不可用

    """
    # the_gpt.Ping()
    return success_response("ping " + str(True))


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
      200:
        description: 密钥更新成功
        schema:
          properties:
            response:
              type: boolean
              description: 表示密钥是否成功更新
      401:
        description: 密钥错误
        schema:
          properties:
            error:
              type: string
              description: 错误信息说明密钥无效

    """

    key = request.json["key"]

    # TODO: update key
    
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
    return success_response("stop " + str(True))


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
    fault_config = request.json["faultConfigInfo"]

    fid, fault_desc = app.the_chat_manager.gen_fault_desc(fault_workflow, fault_config)

    if not fid:
        return error_response("生成故障场景描述失败", 503)

    logging.debug(f"response fault {fid}")
    return success_response({"fault_desc": fault_desc})


@chat_bp.route("/gen_fault_result", methods=["GET"])
def gen_fault_result():
    """
    故障结果，包含以下三个方面：
    - 演练结果
    - 问题分析
    - 运维建议
    ---

    parameters:
      - name: fid
        description: 故障 ID
        in: query
        type: integer
        required: true

    responses:
      401:
        description: 未登录
      404:
        description: 故障 ID 不存在
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

    fid = request.args.get('fid')
    fault = redis.hget('faults', fid).decode('utf-8')
    if not fault:
        logging.error("fault no found")
        return error_response("故障不存在", 404)

    rid, report, analysis = app.the_chat_manager.gen_fault_result(fid)
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
    fault = redis.hget('faults', fid).decode('utf-8')
    if not fault:
        logging.error("fault no found")
        return error_response("故障不存在", 404)

    expectation_text = request.json["expect"]

    eid, expectation = app.the_chat_manager.gen_expect(expectation_text)
    if not eid:
        return error_response("生成用户期望 JSON 失败", 503)

    logging.debug(f"response expectation {eid}")
    # todo: 针对返回 json 需要特殊处理下？
    return success_response(expectation)
