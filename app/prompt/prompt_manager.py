#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：chatops 
@File    ：promptManager.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/12/2 16:23 
'''
import copy
import json
import logging

import pystache

from app.prompt.prompt_static import *
from app.utils.pdata import reform_data, pre_process_data_by_window, pre_process_item
from app.config.dev import DEFAULT_MODEL_TOKEN_CALCULATE

import tiktoken


# 一
def get_prompt_fault_desc(fault_workflow_json):
    return pystache.render(prompt_fault_desc, {'fault_workflow_json': fault_workflow_json})


def get_pre_hot_fault_desc():
    return pre_hot_fault_desc


# 二
def get_prompt_expectation(expectation_text):
    return pystache.render(prompt_expectation, {'expectation_text': expectation_text})


def get_pre_hot_expectation():
    return pre_hot_expectation


# 三
def get_messages_fault_report(fault_result_json, user_expectation, total_num=1500):
    """
    获取功能3（总结错误报告）的messages作为GPT传入参数

    Parameters:
        fault_result_json : 传入的Json格式错误报告
        user_expectation : 传入用户期望
        total_num : 控制GPT输出字符数量，默认1500
    Returns:
        用于与GPT沟通的messages参数
    """
    # 将 JSON 字符串转换为 Python 字典
    fault_result_str = str(fault_result_json)
    fault_result_str = fault_result_str.replace("\'", "\"")
    fault_result_obj_all = json.loads(fault_result_str)

    fault_result_obj = fault_result_obj_all["faultPlayInfo"]
    # 数据规格化
    fault_result_obj = reform_data(fault_result_obj)

    # 清除多余项
    fault_result_obj = pre_process_item(fault_result_obj)

    # 二分查找算法找到合适的window_size
    low, high = 5, 100

    while low <= high:
        mid = (low + high) // 2

        temp_fault_result_obj = copy.deepcopy(fault_result_obj)

        # 数据压缩
        pre_process_data_by_window(temp_fault_result_obj, mid)

        temp_fault_result_json = json.dumps(temp_fault_result_obj)

        messages = [
            {"role": "assistant", "content": example_fault_report},
            {"role": "user", "content": temp_fault_result_json}
        ]

        # messages 的token数量
        token_num = _num_tokens_from_messages(messages)

        if token_num < 11000:
            high = mid - 1  # 缩小窗口大小
        else:
            low = mid + 1  # 增大窗口大小

    # 数据压缩
    pre_process_data_by_window(fault_result_obj, high)
    fault_result_obj = reform_data(fault_result_obj)
    fault_result_obj_all["faultPlayInfo"] = fault_result_obj

    fault_result_info = json.dumps(fault_result_obj_all)
    data = {
        'user_expectation': user_expectation,
        'total_num': total_num,
        'fault_result_info': fault_result_info,
        'example': example_fault_report
    }

    prompt = pystache.render(prompt_fault_report, data)

    messages = [
        {"role": "user", "content": prompt}
    ]

    return messages


def get_prompt_fault_analysis():
    return example_fault_analysis


def get_pre_hot_fault_report():
    """
    获取功能3（总结错误报告）预热prompt
    """
    # prompt 填入用户期望
    data = {
        'user_expectation': "",
        'total_num': 1500,
        'fault_result_info': "",
    }
    # 渲染模板并打印输出
    prompt = pystache.render(prompt_fault_report, data)
    return prompt


# 四
def get_messages_suggestion(fault_desc, user_expectation, fault_report, total_num=1500):
    """
    获取功能4（总结错误报告）的messages作为GPT传入参数

    Parameters:
        fault_desc : 数据库查询本次演练的注入描述
        user_expectation : 从数据库中查询到的用户期望信息
        fault_report : 数据库查询到的错误总结报告
        total_num : 控制GPT输出字符数量，默认1500

    Returns:
        用于与GPT沟通的messages参数
    """

    data_message = {'work_flow': fault_desc,
                    'user_expectation': user_expectation,
                    'fault_report': fault_report,
                    'example': example_suggestion
                    }

    # 渲染模板并打印输出
    message = pystache.render(message_suggestion, data_message)

    messages = [
        {"role": "assistant", "content": example_suggestion},
        {"role": "user", "content": message}
    ]

    return messages


def get_pre_hot_suggestion():
    """
    获取功能4（建议）预热prompt
    """
    data_prompt = {
        "total_num": 1500
    }

    # 渲染模板并打印输出
    return pystache.render(prompt_suggestion, data_prompt)


def _num_tokens_from_messages(messages, model=DEFAULT_MODEL_TOKEN_CALCULATE):
    """

    返回Messages使用的token数量.


    Parameters:
        messages : GPT api输入参数messages
        model : 使用的GPT模型

    Returns:
        token数量
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("[chatops] model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        logging.warning(
            "[chatops] gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return _num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        logging.warning("[chatops] gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return _num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens
