#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python 
@File    ：prompt3.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/11/19 15:15 
'''
from datetime import datetime

from utils.chatWithGPT import gpt_dialogue
from utils.jsonStr import *
import re


def conserve(pre, d, thershold):
    if pre == -1:
        return True
    num = float(d)
    diff = abs(num - pre)
    return thershold <= diff


def is_number(string):
    pattern = r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$'
    return re.match(pattern, string) is not None


def is_timestamp(timestamp):
    try:
        datetime.datetime.fromtimestamp(timestamp)
        return True
    except ValueError:
        return False


def refromObj(data):
    if isinstance(data, dict):
        converted_dict = {}
        for key, value in data.items():
            converted_dict[key] = refromObj(value)  # 递归调用处理嵌套的字典或列表
        return converted_dict
    elif isinstance(data, list):
        converted_list = []
        for item in data:
            converted_list.append(refromObj(item))  # 递归调用处理嵌套的字典或列表
        return converted_list
    elif isinstance(data, float):
        if data < 10:
            return round(data, 2)  # 保留两位小数
        else:
            return int(data)  # 保留整数位

    elif isinstance(data, str):
        if is_number(data):
            return refromObj(float(data))
    return data


file_path = 'faultplayInfo.json'
file_obj = read_json_file(file_path)
file_obj = refromObj(file_obj)


for drill in file_obj:
    drill.pop('paramInfo', None)
    drill.pop('graphData', None)
    drill.pop('graphData', None)
    for M in drill['playPodInfo']:
        M.pop('pressTestInfo', None)
        for index in M['playIndexInfo']:
            dataList = []
            pre = -1
            threshold = 0
            # CPU 指标保留两位小数
            if index['indexName'] == "CPU":
                threshold = 0.15
            elif index['indexName'] == 'receivePackets':
                threshold = 800
            elif index['indexName'] == 'transmitPackets':
                threshold = 800
            elif index['indexName'] == 'receiveBandwidth':
                threshold = 60000
            elif index['indexName'] == 'transmitBandwidth':
                threshold = 60000

            for data in index['data']:
                if conserve(pre, data[1], threshold):
                    dataList.append(data)
                    pre = data[1]

            index['data'] = dataList



prompt = read_file('prompt3.txt')
mes = map_to_json(file_obj)

print(gpt_dialogue(prompt,mes))



