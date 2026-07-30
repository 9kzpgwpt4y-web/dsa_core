import json

# 定义大模型可以调用的工具列表
QUANT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_data",
            "description": "获取指定 A 股股票的历史行情数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "股票代码，如 000001"},
                    "days": {"type": "integer", "description": "获取过去多少天的数据", "default": 30}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_tech_indicators",
            "description": "计算移动平均线(MA)和乖离率(BIAS)等量化指标",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "股票代码"}
                },
                "required": ["symbol"]
            }
        }
    }
]