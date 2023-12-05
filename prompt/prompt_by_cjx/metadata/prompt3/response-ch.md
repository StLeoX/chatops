# 故障注入测试报告分析

## 概述

此报告深入分析了涵盖`user-netdelay`、`frontend-netdelay`和`catalogue-netdelay`的三个核心故障注入演练。在这些演练中，我们专注于CPU使用率、数据包的接收与发送数量（receivePackets和transmitPackets）以及带宽（receiveBandwidth和transmitBandwidth）在关键时刻的表现，以评估系统在面对网络延迟时的表现。

## 1. `user-netdelay` 演练分析

### 数据趋势与峰值分析

- **CPU使用率**：在13时24分54秒，CPU使用率急剧上升至26.0%，远超平时的波动范围（0.17%至0.36%）。
- **数据包数量**：在13时24分54秒，接收数据包数量激增至73853个，发送数据包同一时间达到了102270个，远超平时的波动范围。
- **带宽**：在13时24分54秒，接收带宽急剧上升至12.73MB，发送带宽也达到了20.34MB的顶峰。

## 2. `frontend-netdelay` 演练分析

### 数据趋势与峰值分析

- **CPU使用率**：在13时24分至13时28分的短时间内，CPU使用率急速攀升至63.0%，远超平时的波动范围（0.26%至0.39%）。
- **数据包数量**：在13时28分24秒，接收数据包数飙升至185449个，发送数据包数量也达到了235499个，远超平时的波动范围。
- **带宽**：在13时28分24秒，接收带宽达到了586.14MB，发送带宽也高达189.87MB。

## 3. `catalogue-netdelay` 演练分析

### 数据趋势与峰值分析

- **CPU使用率**：在13时24分至13时28分的短时间内，CPU使用率急速攀升至22.0%，远超平时的波动范围（0.16%至0.23%）。
- **数据包数量**：在13时24分，接收数据包数量急剧上升至65566个，发送数据包数量也达到了92523个，远超平时的波动范围。
- **带宽**：在13时28分24秒，接收带宽达到了586.14MB，发送带宽也达到了189.87MB的高点。

## 总结与系统问题分析

### 用户期望分析

#### 登录模块

- **CPU使用率**：在`user-netdelay`演练中，`user-64856bf58f-7zngw`节点的CPU使用率在13时24分54秒飙升至26.0%，远低于设定的最大阈值80%，此期望满足。

#### 商品目录模块

- **网络带宽接收（receiveBandwidth）**：在`catalogue-netdelay`演练中，`catalogue-6bc98b6c5b-qlfh4`节点的接收带宽在13时28分24秒大幅上升，违反了用户期望中receiveBandwidth应保持在正常水平的要求。
- **网络带宽发送（transmitBandwidth）**：同样，在`catalogue-netdelay`演练中，发送带宽在13时28分24秒显著上升，违反了用户期望中transmitBandwidth应在演练期间保持稳定的要求。
- **网络包接收（receivePackets）**：`catalogue-6bc98b6c5b-qlfh4`节点在13时28分24秒接收数据包数量大幅上升，违反了用户期望中receivePackets应保持在正常范围内的要求。
- **网络包发送（transmitPackets）**：同样，在13时28分24秒，发送数据包数量大幅上升，违反了用户期望中transmitPackets数应保持稳定的要求。

### 系统问题分析

- **CPU使用率突增**：在所有演练中，特定时刻的CPU使用率的显著上升表明，当系统面对故障时，资源利用率大幅提高。
- **数据包数量和带宽的异常增加**：网络故障注入可能导致了数据传输的不稳定性，这可能源于网络拥堵或不恰当的流量管理策略。
- **潜在问题的具体位置**：在`user-netdelay`演练中，13时24分的数据波动突出，显示了系统在应对网络延迟时的脆弱性。同样，在`frontend-netdelay`和`catalogue-netdelay`演练中，13时24分至13时28分的数据波动也指出了网络延迟方面的潜在问题。

综合来看，这些演练结果指出了系统在处理网络延迟方面的潜在缺陷，提示我们需要进一步优化网络流量管理和资源分配策略，以增强系统的稳定性和鲁棒性。