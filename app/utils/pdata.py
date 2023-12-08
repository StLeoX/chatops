import re
import numpy as np

import pandas as pd
from matplotlib import pyplot as plt


def pre_process_data_by_window_item(data, window_size):
    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'value'])

    # 计算移动平均
    df['moving_avg'] = df['value'].rolling(window=window_size, center=True).mean()

    # 检测峰值
    df['peak'] = (df['value'] > df['value'].shift(1)) & (df['value'] > df['value'].shift(-1))

    # 保留峰值和每个窗口中的一个代表性数据点
    df_compressed = df[df['peak'] | (df.index % window_size == 0)]

    # 去除辅助列
    df_compressed = df_compressed.drop(['moving_avg', 'peak'], axis=1)

    # 返回压缩后的数据
    return df_compressed.values.tolist()


def pre_process_item(file_obj):
    # 数据预处理：清除多余项
    for drill in file_obj:
        drill.pop('paramInfo', None)
        for M in drill['playPodInfo']:
            M.pop('pressTestInfo', None)
    return file_obj


def pre_process_data_by_window(file_obj, window_size=10):
    # 数据预处理
    for drill in file_obj:
        for M in drill['playPodInfo']:
            for index in M['playIndexInfo']:
                index['data'] = pre_process_data_by_window_item(index['data'], window_size)
    return file_obj


def format_latex_poly(coefficients):
    terms = []
    degree = len(coefficients) - 1
    for i, coef in enumerate(coefficients):
        if coef == 0:
            continue  # 忽略系数为0的项
        term_degree = degree - i
        coef_str = f"{coef:.1e}" if abs(coef) >= 1000 or abs(coef) < 0.001 else f"{coef:.2f}"
        if term_degree == 0:
            terms.append(coef_str)
        elif term_degree == 1:
            terms.append(f"{coef_str}x")
        else:
            terms.append(f"{coef_str}x^{term_degree}")
    return "f(x)=" + "+".join(terms)


def pre_process_data_by_function(file_obj, segment_size=15, degree=30, draw=False):
    # 数据预处理
    for drill in file_obj:
        drill.pop('paramInfo', None)
        drill.pop('graphData', None)
        for M in drill['playPodInfo']:
            M.pop('pressTestInfo', None)
            for index in M['playIndexInfo']:
                da = index['data']
                raw_data = []
                unix_start = da[0][0]
                # 分段拟合
                for i in range(0, len(da), segment_size):
                    start_time = i + unix_start
                    end_time = start_time + segment_size

                    segment = da[i: i + segment_size]

                    unix_times = [item[0] for item in segment]
                    cpu_params = [float(item[1]) for item in segment]

                    unix_times = np.array(unix_times)
                    cpu_params = np.array(cpu_params)

                    coefficients = np.polyfit(unix_times, cpu_params, degree)
                    fit_function = np.poly1d(coefficients)
                    fit_function_str = format_latex_poly(fit_function)
                    m = {
                        "start": start_time,
                        "end": end_time,
                        "fun": fit_function_str
                    }
                    raw_data.append(m)
                    if draw == True:
                        unix_times_for_plot = np.linspace(min(unix_times), max(unix_times), 500)
                        predicted_cpu_params = fit_function(unix_times_for_plot)
                        plt.plot(unix_times_for_plot, predicted_cpu_params, label=f'Segment {i // 15 + 1}')
                if draw == True:
                    # 绘制原始数据点
                    unix_times_all = [item[0] for item in da]
                    cpu_params_all = [float(item[1]) for item in da]
                    plt.scatter(unix_times_all, cpu_params_all, color='gray', alpha=0.5, label='Original Data')

                    plt.xlabel('Unix Time')
                    plt.ylabel('CPU Parameter')
                    plt.legend()
                    plt.show()
                index['data'] = raw_data
    return file_obj


def reform_data(data):
    if isinstance(data, dict):
        converted_dict = {}
        for key, value in data.items():
            converted_dict[key] = reform_data(value)  # 递归调用处理嵌套的字典或列表
        return converted_dict
    elif isinstance(data, list):
        converted_list = []
        for item in data:
            converted_list.append(reform_data(item))  # 递归调用处理嵌套的字典或列表
        return converted_list
    elif isinstance(data, float):
        if data < 10:
            return round(data, 2)  # 保留两位小数
        else:
            return int(data)  # 保留整数位

    elif isinstance(data, str):
        if is_number(data):
            return reform_data(float(data))
    return data


def is_number(string):
    pattern = r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$'
    return re.match(pattern, string) is not None
