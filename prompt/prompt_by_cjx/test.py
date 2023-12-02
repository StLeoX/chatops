#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：chatops 
@File    ：test.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/12/1 10:16 
'''
import numpy as np
import matplotlib.pyplot as plt
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime
from prompt.prompt_by_cjx.utils.token_utils import num_tokens_from_messages
from prompt.prompt_by_cjx.utils.jsonStr import read_file, read_json_file, map_to_json
from prompt.prompt_by_cjx.utils.p_data import reformObj
from prompt.prompt_by_cjx.utils.chatWithGPT import gpt_dialogue
from prompt.prompt_by_cjx.utils.jsonStr import read_json_file


def format_latex_poly(coefficients):
    terms = []
    degree = len(coefficients) - 1
    for i, coef in enumerate(coefficients):
        term_degree = degree - i
        if coef != 0:  # 只添加非零项
            if term_degree == 0:
                terms.append(f"{coef:.3g}")
            elif term_degree == 1:
                terms.append(f"{coef:.3g}x")
            else:
                terms.append(f"{coef:.3g}x^{{{term_degree}}}")
    return "f(x) = " + " + ".join(terms)


# 读取数据
prompt = read_file('metadata/prompt_base.md')
example = read_file('metadata/example-ch.md')
file_path = 'metadata/faultplayInfo.json'
file_obj = read_json_file(file_path)

print("原始数据token数量：", num_tokens_from_messages(prompt, map_to_json(file_obj)))

import numpy as np
import matplotlib.pyplot as plt

# ... 省略其他导入和函数定义 ...

# 数据预处理
for drill in file_obj:
    drill.pop('paramInfo', None)
    for M in drill['playPodInfo']:
        M.pop('pressTestInfo', None)
        for index in M['playIndexInfo']:
            da = index['data']
            raw_data = []
            # 分段拟合
            for i in range(0, len(da), 15):
                start = i
                end = i + 15
                segment = da[start:end]

                unix_times = [item[0] for item in segment]
                cpu_params = [float(item[1]) for item in segment]

                unix_times = np.array(unix_times)
                cpu_params = np.array(cpu_params)

                coefficients = np.polyfit(unix_times, cpu_params, 20)
                fit_function = np.poly1d(coefficients)
                fit_function_str = format_latex_poly(fit_function)
                m = {
                    "start": start,
                    "end": end,
                    "function": fit_function_str
                }
                raw_data.append(m)
                # 绘制分段拟合
                unix_times_for_plot = np.linspace(min(unix_times), max(unix_times), 500)
                predicted_cpu_params = fit_function(unix_times_for_plot)

                plt.plot(unix_times_for_plot, predicted_cpu_params, label=f'Segment {i // 15 + 1}')
            index['data'] = raw_data
            # 绘制原始数据点
            unix_times_all = [item[0] for item in da]
            cpu_params_all = [float(item[1]) for item in da]
            plt.scatter(unix_times_all, cpu_params_all, color='gray', alpha=0.5, label='Original Data')

            plt.xlabel('Unix Time')
            plt.ylabel('CPU Parameter')
            plt.legend()
            plt.show()

# ... 省略其他代码 ...


print("平移调整后的token数量：", num_tokens_from_messages(prompt, map_to_json(file_obj)))
