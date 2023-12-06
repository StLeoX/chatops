#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：chatops 
@File    ：prompt_static.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/12/6 17:07 
'''
from app.utils.convert import read_file

# 功能三读取文件信息
prompt_fault_report = read_file("resources/prompt3/prompt3.md")
example_fault_report = read_file("resources/prompt3/example3.md")

# 功能四读取文件信息
prompt_suggestion = read_file("resources/prompt4/prompt4.md")
example_suggestion = read_file("resources/prompt4/example4.md")
message_suggestion = read_file("resources/prompt4/input4.md")
