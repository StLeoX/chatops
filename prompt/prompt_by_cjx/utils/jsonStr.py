#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python 
@File    ：jsonStr.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/11/20 16:31 
'''

import json


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        return file_content

def get_api_key():
    openai_key_file = "../metadata/openai_key.json"
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

def map_to_json(m):
    return json.dumps(m)
