# ChatOps

## 项目概述

ChatOps 是一款面向电网故障注入场景的运维助手，具有以下四个方面的功能：

- 故障场景描述

- 用户期望描述

- 故障结果描述

- 生成运维建议

### 项目结构

`doc` 中存放项目的共享文档，包括项目设计文档、测试文档、提示词文档等等

`prompt`存放负责提示词开发同学的代码

`rerouces`存放资源文件

## 其他

### 仓库管理

`master` 分支受保护，禁止直接推送代码，请从其他分支提 PR。

目前 PR 的审查规则是：两个人代码过审、两个人测试过审。

issue 展示不使用，项目管理全在 pingcode 上。

### 使用
运行镜像：
```shell
docker run -e FLASK_DEBUG="False" BASE_URL="" OPENAI_API_KEY="" image_name
```

如果用网络代理，添加环境变量 `http_proxy` 和 `https_proxy`。
