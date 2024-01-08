#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：chatops 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/11/28 22:26 
'''
import numpy as np
from cvxopt import matrix, solvers

# 训练数据和标签
X = np.array([[3, 3], [4, 3], [1, 1]])
y = np.array([1, 1, -1])

# 计算内积矩阵
n_samples = X.shape[0]
K = np.zeros((n_samples, n_samples))
for i in range(n_samples):
    for j in range(n_samples):
        K[i, j] = np.dot(X[i], X[j])

# 构建二次规划的参数
P = matrix(np.outer(y, y) * K)
q = matrix(-np.ones(n_samples))
G = matrix(-np.eye(n_samples))
h = matrix(np.zeros(n_samples))
A = matrix(y, (1, n_samples), 'd')
b = matrix(0.0)

# 解二次规划
solution = solvers.qp(P, q, G, h, A, b)
alphas = np.ravel(solution['x'])

# 其他代码保持不变

# 计算w
# 首先调整alphas和y的形状以匹配X
alphas_expanded = alphas[:, None]  # 将alphas从形状(3,)变为形状(3,1)
y_expanded = y[:, None]  # 将y从形状(3,)变为形状(3,1)

# 现在进行元素乘法并求和
w = np.sum(alphas_expanded * y_expanded * X, axis=0)

# 计算b
# 选择一个支持向量来计算b
# 这里我们选择第一个非零alpha对应的样本
sv = np.where(alphas > 1e-5)[0][0]
b = y[sv] - np.dot(w, X[sv])

# 输出结果
print("Lagrange multipliers (alphas):", alphas)
print("w:", w)
print("b:", b)
