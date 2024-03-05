# Other modules
import json

import pytest

# Local modules
from app import create_app

from test.utils.mocker import RequestMocker


@pytest.fixture
def app():
    app = create_app()
    return app


# todo(fxc)
def test_gpt_ping(app):
    with app.test_client() as client:
        response = client.get("/v1/chat/gpt_ping")

        print('deb response', response.json)

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "ping True"


def test_gpt_update_key(app):
    with app.test_client() as client:
        # 模拟发送包含 "key" 的 JSON 请求
        response = client.post("/v1/chat/gpt_update_key", json={"key": "new_key"})

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "echo key new_key"


def test_gpt_stop(app):
    with app.test_client() as client:
        response = client.get("/v1/chat/gpt_stop")

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "stop True"


def test_gen_fault_desc(app):
    with app.test_client() as client:
        workflowInfo1 = RequestMocker.echo_request_workflow('username').json
        faultConfigInfo1 = RequestMocker.echo_request_fault_config('username').json

        print('deb workflowInfo1', workflowInfo1)

        fault1 = {"fault":
                      {"workflowInfo": workflowInfo1,
                       "faultConfigInfo": faultConfigInfo1}}
        # 模拟发送包含 "fault" 的 JSON 请求
        response = client.post("/v1/chat/gen_fault_desc",
                               json=fault1)

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "fault_id 123"


def test_gen_expect(app):
    with app.test_client() as client:
        # 模拟发送包含 "fid" 的 JSON 请求
        response = client.post("/v1/chat/gen_expect", json={"fid": "123"})

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "expect nothing"


def test_gen_fault_report(app):
    with app.test_client() as client:
        # 模拟发送包含 "fid" 的 JSON 请求
        response = client.post("/v1/chat/gen_fault_report", json={"fid": "123"})

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "report nothing"


def test_gen_advice(app):
    with app.test_client() as client:
        # 模拟发送包含 "fid" 的 JSON 请求
        response = client.post("/v1/chat/gen_advice", json={"fid": "123"})

        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert response.json["data"] == "advice nothing"
