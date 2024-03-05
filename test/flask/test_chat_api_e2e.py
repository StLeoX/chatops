# 端到端模拟 cURL 请求

import requests
import json


########### 1

# 确保 flask 在运行
def test_gpt_ping1():
    response = requests.get('http://127.0.0.1:9999/v1/chat/gpt_ping')
    assert response.status_code == 200
    print(response.json())


# 确保 flask 在运行
def test_gen_fault_desc1():
    with open(r'/root/Source/python/chatops/test/prompt/data_username/workflowInfo/workflowInfo.json') as f:
        workflowInfo1 = json.load(f)
    faultConfigInfo1 = {"dummy": "dummy"}

    fault1 = {"workflowInfo": workflowInfo1,
              "faultConfigInfo": faultConfigInfo1}

    response1 = requests.post('http://127.0.0.1:9999/v1/chat/gen_fault_desc', json=fault1)
    assert response1.status_code == 200
    print(response1.json())


# 确保 flask 在运行
def test_gen_fault_result1():
    with open(r'/root/Source/python/chatops/test/prompt/data_username/faultplayInfo/faultplayInfo.json') as f:
        faultPlayInfo1 = json.load(f)

    print("first run test_gen_fault_desc1")
    test_gen_fault_desc1()
    print("now focusing fid is 2")

    fault1 = {"fault": {
        "fid": 2,
        "faultPlayInfo": faultPlayInfo1
    }}
    response1 = requests.post("http://127.0.0.1:9999/v1/chat/gen_fault_result", json=fault1)
    assert response1.status_code == 200
    print(response1.json())


# 确保 flask 在运行
# 2 和 1 的区别在已经存在 fid2
def test_gen_fault_result2():
    with open(r'/root/Source/python/chatops/test/prompt/data_username/faultplayInfo/faultplayInfo.json') as f:
        faultPlayInfo1 = json.load(f)

    fault1 = {"fault": {
        "fid": 2,
        "faultPlayInfo": faultPlayInfo1
    }}
    response1 = requests.post("http://127.0.0.1:9999/v1/chat/gen_fault_result", json=fault1)
    assert response1.status_code == 200
    print(response1.json())
