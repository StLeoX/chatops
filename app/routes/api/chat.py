import redis
from flask import Blueprint, request, abort
from app.utils.api import success_response

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

    # todo(xla)
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

    # todo(xla)
    fault_id = request.json["fid"]
    # expectation = redis.Redis[""]
    return success_response("report nothing")


@chat_bp.route("/gen_advice", methods=["POST"])
def gen_advice():
    """
    生成运维建议
    fault_id
    boolean, string
    """

    # todo(xla)
    fault_id = request.json["fid"]
    # expectation = redis.Redis[""]
    # fault_report = redis.Redis[""]
    return success_response("advice nothing")
