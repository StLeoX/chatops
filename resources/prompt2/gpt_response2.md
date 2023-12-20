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