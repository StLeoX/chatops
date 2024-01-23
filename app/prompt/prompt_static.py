#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：chatops 
@File    ：prompt_static.py
@IDE     ：PyCharm 
@Author  ：Cjx_0723
@Date    ：2023/12/6 17:07 
'''

# 功能一：故障场景描述
prompt_fault_desc = r'''
你是一名经验丰富的服务器运维专家，目前手头有一份关于服务器故障注入测试的流程图数据以及故障注入过程中的压力测试数据。
在流程图数据中，使用的是JSON格式来描述本次故障注入的整个流程，本次故障注入涉及到多个故障演练，每一个故障演练之间有着串行或是并行的执行流程，流程图数据为：{{work_flow_info}}
每一个故障演练以及该演练的子动作的开始、结束时间也将给出, 该数据为： {{fault_config_json}}
本次的分析需要你描述本次演练场景，输出的内容一定要包含下面几点：

1. **演练目的**：描述演练的主要目标，这点在流程图数据的chaosType中有所体现，我需要你详细分析该演练的目标。同时我也希望你能明确演练的业务或技术目的。
2. **演练范围**：首先介绍每一场演练的演练ID号；其次介绍本次涉及是涉及到的具体服务或是整个系统，这部分希望论述哪一场演练涉及到了哪一些服务并基于已有数据描述演练。同时总结每一场演练涉及到的故障类型。最后每一场演练涉及到的故障描述 (注入什么故障、针对什么设备、注入故障规模大小等等)
3. **演练流程图描述**：详细描述整体注入的执行流程，首先介绍本次故障注入整体是串行还是并行，是串行的话其顺序依次描述每一个故障演练的细节，如果是并行需要说明哪些故障演练是并发执行的。其次还需要输出本次演练的具体执行细节，包括本次故障注入涉及到哪些演练了哪些演练,每一个演练的具体执行的开始时间和结束时间是多少,结束的原因是什么。最后具体来谈一谈每一个演练的每一个子动作开始、结束的具体时间是什么时候。

下面输出报告一定要满足的的要求：

1. 在表示数据时注意加上相应的单位，单位有下面要求：unix时间精确到小时分钟，例如"13时24分"，我不希望看到例如1699255304的Unix时间;带宽单位是B，我想你讲带宽转换为近似的数值能够让用户易于阅读，例如7039B转换为7kB。
2. 现在你的回复是一篇报告，不允许出现你跟我对话的任何内容！
3. 回答字数多于1500字，生成的格式为markdown格式，输出文本允许使用的markdown语法仅仅包括标题语法，呈现输出的层次结构，不允许出现"1. 2. 3. " 这样的有序列表！也不允许出现"- - - -" 这样的无序列表！
4. 总结性的语句不需要说明，按照上述要求介绍完演练目的、演练范围以及演练流程图介绍后就可以停止回复了，不需要总结！
5. 样例只是规定你的输出格式，输出内容一定要基于我提供的数据进行分析，剖析数据的深层含义后输出内容，这点必须要做到！
'''

prompt_fault_desc_example = r'''
# 服务器故障注入测试报告

## 演练目的

本次服务器故障注入测试的主要目标是对系统的稳定性和可靠性进行检验。通过模拟网络延迟的故障，我们可以观察系统在不同网络状态下的表现，从而评估系统的健壮性和故障恢复能力。演练的业务目的是确保在真实的故障情况发生时，系统能够保持正常运行或快速恢复，减少业务中断的时间和影响。技术目的则是验证和优化故障检测、定位、恢复等流程，提升系统的整体运维能力。

在流程图数据中，chaosType为"NetworkChaos"，表明本次演练主要关注网络层面的故障模拟，具体是通过注入网络延迟来模拟不稳定的网络环境，从而达到测试和提高系统容错性、稳定性的目的。

## 演练范围

### 故障演练1: 用户服务网络延迟

- **故障演练ID**: fault-18c36a2d
- **服务范围**: 用户服务（user）
- **故障类型**: 网络延迟（NetworkChaos）
- **故障描述**: 本演练将500毫秒的固定延迟和500毫秒的抖动及50%的相关性注入用户服务。目标是评估网络延迟对用户服务稳定性和性能的影响。故障覆盖所有标记为"name: user"的服务，属于命名空间"sock-shop"。

### 故障演练2: 前端服务网络延迟

- **故障演练ID**: fault-bc93c7c9
- **服务范围**: 前端服务（front-end）
- **故障类型**: 网络延迟（NetworkChaos）
- **故障描述**: 本演练将500毫秒的固定延迟和500毫秒的抖动及50%的相关性注入前端服务。目标是评估网络延迟对于前端服务稳定性和用户交互体验的影响。通过模拟这种延迟，可以观察并分析前端服务在不理想的网络条件下的表现和容错机制。故障覆盖所有标记为"name: front-end"的服务，属于命名空间"sock-shop"。

### 故障演练3: 产品目录服务网络延迟

- **故障演练ID**: fault-3da791f4
- **服务范围**: 产品目录服务（catalogue）
- **故障类型**: 网络延迟（NetworkChaos）
- **故障描述**: 本演练向产品目录服务注入500毫秒的固定延迟和500毫秒的抖动，以及50%的相关性。目标是评估网络延迟对产品目录服务的稳定性和响应时间的影响。故障覆盖所有标记为"name: catalogue"的服务，属于命名空间"sock-shop"。

## 演练流程图描述

### 故障注入执行流程

本次故障注入整体是并行执行的，具体执行流程如下：

1. **并行演练启动**: 三个故障演练（fault-18c36a2d、fault-bc93c7c9、fault-3da791f4）几乎同时开始，展现了在实际环境中可能同时发生的多点故障场景。
2. **故障注入与恢复**: 每个故障演练包含了故障注入、等待和恢复三个步骤，模拟了从故障发生到处理恢复的完整过程。

### 故障演练细节

#### 整体演练细节

- **入口ID**: "paraller-490912"
- **执行类型**: Parallel

#### 各演练细节

- **fault-18c36a2d**:
  - 开始时间: 2023-11-06 07:22:14
  - 结束时间: 2023-11-06 07:27:16
  - 结束原因: 正常完成
  - 子动作时间:
    - 故障注入: 2023-11-06 07:22:14 - 2023-11-06 07:27:18
    - 等待: 2023-11-06 07:22:16 - 2023-11-06 07:27:18
    - 恢复: 2023-11-06 07:27:16 - 2023-11-06 07:27:18

- **fault-bc93c7c9**:
  - 开始时间: 2023-11-06 07:22:14
  - 结束时间: 2023-11-06 07:27:17
  - 结束原因: 正常完成
  - 子动作时间:
    - 故障注入: 2023-11-06 07:22:14 - 2023-11-06 07:27:18
    - 等待: 2023-11-06 07:22:17 - 2023-11-06 07:27:18
    - 恢复: 2023-11-06 07:27:17 - 2023-11-06 07:27:18

- **fault-3da791f4

**:
  - 开始时间: 2023-11-06 07:22:14
  - 结束时间: 2023-11-06 07:27:18
  - 结束原因: 正常完成
  - 子动作时间:
    - 故障注入: 2023-11-06 07:22:15 - 2023-11-06 07:27:18
    - 等待: 2023-11-06 07:22:17 - 2023-11-06 07:27:18
    - 恢复: 2023-11-06 07:27:18 - 2023-11-06 07:27:18

通过详细的时间记录和步骤划分，我们可以对每个演练的执行过程有一个清晰的了解，从而更好地评估演练的效果和系统的表现。每个故障演练都经历了注入、等待和恢复三个阶段，反映了在真实场景中处理故障的一般流程。
'''

pre_hot_fault_desc = r'''
您是一个有用的人工智能，专门在Python中处理JSON数据。
您可以解析JSON字符串、访问值、修改数据和完美地格式化JSON。
您的任务是解析JSON字符串，并访问与给定键关联的值。
'''

# 功能二：用户期望描述
prompt_expectation = r'''
你将会被提供一段由自然语言写成的文本，代表用户对一个应用的目标期望。
执行以下任务：
1 - 把这些以JSON对象的形式输出，JSON 字段使用英文，例如成功率使用"success_rate"，登录模块使用"login_module"。
2 - "note"字段可以说明一些数值的单位或者其他用户的期望需要说明的。\
3 - 把 "80%"、"±10%"、"2秒" 等表示为字符串的转化为0.8、0.1、2这些数值型\
4 - 下面是登录模块(login_module)的文本：{{expectation_text}}
'''

pre_hot_expectation = r'''
你是一个有帮助的助手，旨在逐点提取基本信息，并使用这些基本信息将用户输入的自然语言转换成JSON格式。
'''

example_expectation_text = r'''
登录模块：
{
CPU使用率：登录节点的CPU使用率不应超过设定的最大阈值（如80%），以避免过载导致登录延迟。\
TPS（每秒事务数）：在网络抖动演练期间，系统的TPS应维持在正常范围内的±10%，以确保处理能力不受显著影响。\
成功率：登录请求的成功率应高于设定的最低标准（如99%），确保用户能够成功登录。\
响应时间：登录请求的响应时间应在2秒以内，超时重试机制应在5秒后启动。\
}
商品目录模块：
{
网络带宽接收（receiveBandwidth）：即便在网络延迟期间，receiveBandwidth应保持在正常水平的±50%以内，确保足够的数据吞吐量。\
网络带宽发送（transmitBandwidth）：transmitBandwidth应该稳定，在演练期间不会有大幅下降，保证商品信息能够及时更新。\
网络包接收（receivePackets）：receivePackets数应保持在正常范围内，允许的偏差为±60%。\
网络包发送（transmitPackets）：transmitPackets数应稳定，不会因网络抖动导致大量数据包丢失.\
}
'''

example_expectation_json = r'''
{
  "login_module": {
    "cpu_usage": {
      "description": "登录节点的CPU使用率",
      "max_threshold": "0.8",
      "note": "不应超过设定的最大阈值，以避免过载导致登录延迟"
    },
    "tps": {
      "description": "每秒事务数（TPS）",
      "normal_range_variation": "0.1",
      "note": "在网络抖动演练期间，应维持在正常范围内的±10%，以确保处理能力不受显著影响"
    },
    "success_rate": {
      "description": "登录请求的成功率",
      "min_standard": "0.99",
      "note": "应高于设定的最低标准，确保用户能够成功登录"
    },
    "response_time": {
      "description": "登录请求的响应时间",
      "max_time": "2",
      "retry_mechanism_start": "5",
      "note": "时间的单位是秒"
    }
  }
}
'''

# 功能三：演练报告 + 问题分析
prompt_fault_report = r"""
您是一名经验丰富的服务器运维专家，手头有一份关于服务器故障注入测试检测的数据。这份数据包含了多次故障注入演练的详细信息，每个演练的名称和一系列系统时序数据都已包含在内。您的任务是根据这些数据进行全面细致的分析。
在分析开始之前，请介绍本次报告的内容，包括所有演练的名称和您的分析方法。报告的分析内容应包括但不限于以下几个方面：

1. 数据趋势分析：观察时序的长期趋势，包括在故障注入前后的变化，特别注意在故障注入前后时序数据波动情况。这部分必须需要包括下面的数据：正常数据波动区间与异常数据波动区间，描述何时至何时数据产生波动，数据波动的范围是多少
2. 峰值分析：数据峰值，峰值需要说明在具体时间达到了多少的数值

在完成对每一次单次演练的分析后，请对整个故障注入测试进行总结。这包括所有演练的汇总分析这包括所有演练的汇总分析，基于上述分析结果，写出总结。
总结需要包含下面的内容：    
1. 基于提供的数据和用户期望，分析本次演练的结果是否符合用户期望，如不符合则具体说明在何时用户期望因什么哪次注入而没有被满足，这部分需要对每一条用户期望单独分析，如果用户期望涉及到的数据没有提供，则该条用户期望不分析,用户期望如下：{{user_expectation}}
2. 这部分需要概括本次输出的大部分内容，总结可以具体谈一谈每一个注入的情况，并汇总给定数据中潜在的系统问题并加以分析，分析系统问题时希望你能告诉我在哪些演练的哪些时间段数据呈现出此问题。

你输出内容必须要满足的的要求：

1. 输出格式必须参考模板，模板如下:example={{{example}}},但请注意！模板中的数据和文本不应作为分析依据，仅作为格式参考。 
2. 现在你的回复是一篇报告，不允许出现你跟我对话的任何内容！输出的内容应该是完整的，不能出现任何形式的内容省略！输出文本的格式为markdown格式，输出文本允许使用的markdown语法仅仅包括标题语法
3. 所有的数据加上相应的单位,输出的时序数据时必须说明其出现的时间,这可以在接下来提供给你的data数据中分析得到,我提供给你的是[时间,时序数据]对
4. 对于异常模式识别模块，在每一个异常模式论述中添加该异常的具体位置，在哪个演练中出现在某个时间段
5. 本次输出的内容不少于{{{total_num}}}字！我希望分析能够更加具体！

现在请你根据上述要求分析下面的数据,注意！接下来出现的数据才是你需要分析的数据,之前出现的任何数据都不需要分析仅供参考,之前出现的任何数据都不能作为输出内容的参考依据！接下来需要分析的数据数据如下：data1 = {{{fault_result_info}}} ,data1中的数据才是你需要分析的全部数据,请你直接忽略example中的内容
"""

example_fault_report = r"""
# 故障注入测试报告分析

## 概述

此报告深入分析了涵盖`user-netdelay`、`frontend-netdelay`和`catalogue-netdelay`的三个核心故障注入演练。在这些演练中，我们专注于CPU使用率、数据包的接收与发送数量（receivePackets和transmitPackets）以及带宽（receiveBandwidth和transmitBandwidth）在关键时刻的表现，以评估系统在面对网络延迟时的表现。

## 1\. `user-netdelay` 演练分析

### 1\. `user-netdelay` 演练

-   **CPU使用率分析**：
    
    -   在正常情况下，CPU使用率保持在0.17%至0.36%的稳定范围内。
    -   但在XXXX，我们观察到一个异常峰值，CPU使用率突然飙升至26.0%，持续了大约10秒，这是一个显著的异常表现。
-   **数据包处理（receivePackets和transmitPackets）**：
    
    -   正常状态下，接收的数据包数量在343至910个之间波动，发送的数据包数量在293至916个之间。
    -   然而，在XXXX，接收数据包数量激增至73853个，而发送数据包数量也同步上升至102270个，持续了约13秒，表明了一个明显的网络流量异常。
-   **带宽使用（receiveBandwidth和transmitBandwidth）**：
    
    -   在日常运行中，接收带宽维持在31.5kB至80.3kB，发送带宽在34.5kB至101.7kB。
    -   但XXXX发生了显著变化，接收带宽急剧上升至12.73MB，发送带宽也达到20.34MB，这一异常状态持续了约15秒，显示了网络延迟的显著影响。

### 2\. `frontend-netdelay` 演练

-   **CPU使用率分析**：
    
    -   平时CPU使用率在0.26%至0.39%之间波动。
    -   但在XXXX，出现了异常，CPU使用率急升至63.0%，并在大约40秒后恢复正常，这表明了显著的性能波动。
-   **数据包处理（receivePackets和transmitPackets）**：
    
    -   正常情况下，接收和发送数据包数量分别维持在266至696个和233至603个之间。
    -   然而，在XXXX，接收数据包数量飙升至185449个，发送数据包数量也增至235499个，持续了约32秒，反映出网络延迟引起的显著流量增加。
-   **带宽使用（receiveBandwidth和transmitBandwidth）**：
    
    -   通常接收带宽在20.9kB至55.7kB之间，发送带宽在31.5kB至81.9kB。
    -   但在XXXX，接收带宽飙升至586.14MB，发送带宽也达到了189.87MB，这种异常状态持续了约32秒，表明了网络延迟对带宽的巨大影响。

### 3\. `catalogue-netdelay` 演练

-   **CPU使用率分析**：
    
    -   一般来说，CPU使用率保持在0.16%至0.23%之间。
    -   但在XXXX，出现了显著波动，CPU使用率升至22.0%，这一异常持续了约45秒，显示了处理能力的临时压力。
-   **数据包处理（receivePackets和transmitPackets）**：
    
    -   正常运行时，接收和发送数据包数量相对平稳。
    -   异常出现在XXXX，接收数据包数量增至65566个，发送数据包达到92523个，这一变化持续了约38秒，反映了网络延迟期间数据包处理的显著变化。
-   **带宽使用（receiveBandwidth和transmitBandwidth）**：
    
    -   在正常情况下，接收带宽和发送带宽保持稳定。
    -   但在XXXX，带宽使用发生了显著变化，接收带宽达到了586.14MB，发送带宽为189.87MB，这一状态持续了约40秒，凸显了带宽使用在网络延迟期间的异常表现。

## 总结与系统问题分析

### 用户期望分析

#### 登录模块

-   **CPU使用率**：在`user-netdelay`演练中，`user-64856bf58f-7zngw`节点的CPU使用率在XXXX飙升至26.0%，远低于设定的最大阈值80%，此期望满足。

#### 商品目录模块

-   **网络带宽接收（receiveBandwidth）**：在`catalogue-netdelay`演练中，`catalogue-6bc98b6c5b-qlfh4`节点的接收带宽在XXXX大幅上升，远超正常水平。这表明receiveBandwidth在网络延迟期间没有保持在正常水平的±20%以内，不符合用户期望。
-   **网络带宽发送（transmitBandwidth）**：同样，在`catalogue-netdelay`演练中，发送带宽在XXXX显著上升，违反了用户期望中transmitBandwidth应在演练期间保持稳定的要求。
-   **网络包接收（receivePackets）**：`catalogue-6bc98b6c5b-qlfh4`节点在XXXX接收数据包数量大幅上升，远超正常范围，不符合用户期望中receivePackets应保持在正常范围内的要求。
-   **网络包发送（transmitPackets）**：同样，在XXXX，发送数据包数量大幅上升，超出正常范围，违反了用户期望中transmitPackets数应保持稳定的要求。
### 系统问题分析

-   **CPU使用率突增**：在所有演练中，特定时刻的CPU使用率的显著上升表明，当系统面对故障时，资源利用率大幅提高。
-   **数据包数量和带宽的异常增加**：网络故障注入可能导致了数据传输的不稳定性，这可能源于网络拥堵或不恰当的流量管理策略。
-   **潜在问题的具体位置**：在`user-netdelay`演练中，XXXX的数据波动突出，显示了系统在应对网络延迟时的脆弱性。同样，在`frontend-netdelay`和`catalogue-netdelay`演练中，XXXX至XXXX的数据波动也指出了网络延迟方面的潜在问题。

综合来看，这些演练结果指出了系统在处理网络延迟方面的潜在缺陷，提示我们需要进一步优化网络流量管理和资源分配策略，以增强系统的稳定性和鲁棒性。
"""

example_fault_analysis = r"""
# 系统问题分析与总结

## 用户期望分析

### 登录模块

-   **CPU使用率**：在`user-netdelay`演练中，`user-64856bf58f-7zngw`节点的CPU使用率在2023-11-06 15:21:11飙升至26.0%，远低于设定的最大阈值80%，此期望满足。

### 商品目录模块

-   **网络带宽接收（receiveBandwidth）**：在`catalogue-netdelay`演练中，`catalogue-6bc98b6c5b-qlfh4`节点的接收带宽在2023-11-06 15:21:21大幅上升，远超正常水平。这表明receiveBandwidth在网络延迟期间没有保持在正常水平的±20%以内，不符合用户期望。
-   **网络带宽发送（transmitBandwidth）**：同样，在`catalogue-netdelay`演练中，发送带宽在2023-11-06 15:21:31显著上升，违反了用户期望中transmitBandwidth应在演练期间保持稳定的要求。
-   **网络包接收（receivePackets）**：`catalogue-6bc98b6c5b-qlfh4`节点在2023-11-06 15:21:32接收数据包数量大幅上升，远超正常范围，不符合用户期望中receivePackets应保持在正常范围内的要求。
-   **网络包发送（transmitPackets）**：同样，在2023-11-06 15:21:44，发送数据包数量大幅上升，超出正常范围，违反了用户期望中transmitPackets数应保持稳定的要求。

## 系统问题分析

-   **CPU使用率突增**：在所有演练中，特定时刻的CPU使用率的显著上升表明，当系统面对故障时，资源利用率大幅提高。
-   **数据包数量和带宽的异常增加**：网络故障注入可能导致了数据传输的不稳定性，这可能源于网络拥堵或不恰当的流量管理策略。
-   **潜在问题的具体位置**：在`user-netdelay`演练中，2023-11-06 15:21:11的数据波动突出，显示了系统在应对网络延迟时的脆弱性。同样，在`frontend-netdelay`和`catalogue-netdelay`演练中，2023-11-06 15:21:48至2023-11-06 15:24:48的数据波动也指出了网络延迟方面的潜在问题。

综合来看，这些演练结果指出了系统在处理网络延迟方面的潜在缺陷，提示我们需要进一步优化网络流量管理和资源分配策略，以增强系统的稳定性和鲁棒性。
"""

# 功能四读取文件信息
prompt_suggestion = r"""
现在你扮演一名经验丰富的服务器运维专家，负责分析故障注入测试的结果。公司将提供给你详细的故障注入信息，包括：

-   **故障注入的工作流程**：请详细描述本次演练中涉及到的每个故障注入的流程，包括注入的类型、参数和执行过程。
    
-   **故障注入的总结**：基于本次演练的数据，分析故障注入对系统性能的影响，以及这些数据变化对用户期望和系统潜在问题的指示。
    
-   **满足用户期望的优化建议**：请根据故障注入的总结，提出如何改进系统以更好地满足用户期望。如果系统表现符合用户期望，给出进一步的优化建议；如果不符合，指出问题所在并详细提出改进措施。

您的专业分析和建议将对我们的系统优化至关重要，根据我提供给您的文本,输出详细的建议报告,只需要输出您对系统的建议,但建议需要围绕用户期望展开，即如何优化已经满足的用户期望以及如何提升系统在某些方面的表现从而满足那些没有被满足的用户期望。我希望您提供的建议不仅仅是宽泛的说词例如"提升系统吞吐率"，而是具体到如何实现，实现的工具或是方法有哪些，这些优化方法将对系统带来哪些改观。
因为您是这方面的专家，因此我希望您输出的内容能够尽可能地详细,对于每一条可优化的点我也希望您提供不止一条建议，建议的内容也要具体到如何实现！

请确保：

-   输出内容详尽且清晰，字数不少于{{total_num}}字。
-   所有时间数据需转换为标准时间格式，如“2023-11-06 15:21:44”，并确保所有数据具有明确的单位。
-   您的回答应专注于任务内容，避免包含与任务无关的对话内容。
-   输出的内容只包含基于用户期望的系统建议，其他内容只需要分析不需要输出！不需要输出故障注入的工作流程以及故障注入总结！
"""

# 功能四：生成运维建议
example_suggestion = r"""
根据您提供的故障注入测试数据和用户期望，以下是一系列的系统优化建议，旨在提高系统性能，确保它们符合或超过用户的期望：

### 登录模块优化

1.  **CPU使用率**：虽然CPU使用率未超过设定的最大阈值80%，但为了进一步优化性能和响应时间，建议对登录模块进行资源分配优化。确保有足够的CPU资源来处理高峰期的请求。可以考虑实施动态资源分配策略，根据负载情况自动调整资源分配。
    
2.  **TPS和成功率**：提高每秒事务数(TPS)和登录请求的成功率可以通过增强服务器的处理能力和网络带宽实现。考虑使用负载均衡和更高效的请求处理算法来提高处理能力。同时，优化后端服务的处理逻辑，减少不必要的数据库查询和计算，从而提升请求的处理速度和成功率。
    
3.  **响应时间优化**：针对响应时间的优化，可以通过实现更高效的缓存策略和数据库查询优化来降低响应时间。此外，对前端进行代码优化，减少不必要的数据加载和渲染，也将有助于减少响应时间。
    

### 商品目录模块优化

1.  **网络带宽接收和发送**：在网络延迟期间，receiveBandwidth和transmitBandwidth的表现未达到用户期望。考虑引入更高效的数据压缩算法和优化网络协议栈，以减少数据包大小和提高带宽利用率。此外，可以考虑使用更高效的网络设备和升级现有的网络基础设施。
    
2.  **网络包接收和发送**：为了稳定网络包的接收和发送，建议优化网络队列管理策略，使用更智能的流量控制机制，以及实现更有效的数据包调度策略。例如，实现基于优先级的队列管理，确保关键数据包能够优先处理。
    

### 前端模块优化

1.  **本地数据缓存**：加强本地缓存机制，确保在网络抖动期间，用户最常访问的数据能够被高效缓存和快速访问。考虑使用服务工作线程(Service Workers)来提升在离线状态下的数据获取能力。此外，对于重要的用户界面元素，采用懒加载技术，减少初次加载时的数据传输量。

### 其他综合优化措施

1.  **故障容忍和冗余**：在系统架构中实现更多的故障容忍机制，如多地域部署和数据备份策略，以保证在面对网络延迟等故障时，系统能够快速恢复和保持运行。
    
2.  **监控和自动化**：加强系统监控，实现实时性能监控和自动化故障检测。在检测到性能下降时，自动启动优化或恢复流程。
    
3.  **持续测试和优化**：定期进行类似的故障注入测试，并根据测试结果不断调整和优化系统。利用这些测试来预测和预防可能的性能瓶颈。
    

通过实施这些优化策略，系统不仅能够满足当前的用户期望，还能为未来可能出现的更严格要求做好准备。
"""

message_suggestion = r"""
接下来我将输入您需要分析的内容，与之前介绍中的一样，我的数据将包括：故障注入的工作流程、客户所提出的期望、故障注入总结，公司为了规范你的输出内容，请你输出的建议参考模板
首先本次故障注入的工作流程：{{work_flow}}
本次客户所提出的期望是：{{user_expectation}}
本次故障注入总结：{{fault_report}}
生成的建议输出模板可以参考：{{example}}
"""
