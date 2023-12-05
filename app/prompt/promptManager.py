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

import pystache

from app.utils.convert import read_file
from app.utils.pdata import reform_data, pre_process_data_by_window, pre_process_item
import tiktoken


def get_messages_summary_fault_report(fault_result_json, user_expectation):
    """
    获取功能3（总结错误报告）的messages作为GPT传入参数

    Parameters:
        fault_result_json : 传入的Json格式错误报告
        user_expectation ： 传入用户期望
    Returns:
        用于与GPT沟通的messages参数
    """

    # 读取文件信息
    prompt = read_file("resources/prompt3/prompt3.md")
    example = read_file("resources/prompt3/example3.md")

    # prompt 填入用户期望
    data = {
        'user_expectation': user_expectation
    }
    # 渲染模板并打印输出
    prompt = pystache.render(prompt, data)

    # 数据规格化
    fault_result_json = reform_data(fault_result_json)

    # 将 JSON 字符串转换为 Python 字典
    fault_result_obj = json.loads(fault_result_json)
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
            {"role": "system", "content": prompt},
            {"role": "user", "content": "run"},
            {"role": "assistant", "content": example},
            {"role": "user", "content": temp_fault_result_json}
        ]

        # messages 的token数量
        token_num = num_tokens_from_messages(messages)

        if token_num < 14000:
            high = mid - 1  # 缩小窗口大小
        else:
            low = mid + 1  # 增大窗口大小

    # 数据压缩
    pre_process_data_by_window(fault_result_obj, high)

    fault_result_obj = json.dumps(fault_result_obj)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "run"},
        {"role": "assistant", "content": example},
        {"role": "user", "content": fault_result_obj}
    ]

    return messages


def get_messages_suggestion(fault_desc, user_expectation, fault_report):
    """
    获取功能3（总结错误报告）的messages作为GPT传入参数

    Parameters:
        fault_desc : 数据库查询本次演练的注入描述
        user_expectation : 从数据库中查询到的用户期望信息
        fault_report : 数据库查询到的错误总结报告

    Returns:
        用于与GPT沟通的messages参数
    """

    # 读取文件信息
    prompt = read_file("resources/prompt4/prompt4.md")
    example = read_file("resources/prompt4/example4.md")
    message = read_file("resources/prompt4/input4.md")

    data = {'work_flow': fault_desc,
            'user_expectation': user_expectation,
            'fault_report': fault_report,
            'example': example
            }

    # 渲染模板并打印输出
    message = pystache.render(message, data)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "run"},
        {"role": "assistant", "content": example},
        {"role": "user", "content": message}
    ]

    return messages


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
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
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
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