import os
import json
from dotenv import load_dotenv
from litellm import completion
from src.utils.logger import logger

# 加载 .env 中的 DEEPSEEK_API_KEY
load_dotenv()

class FinanceAgent:
    def __init__(self):
        # 使用 DeepSeek 官方模型路径 (通过 litellm 转发)
        self.model = "deepseek/deepseek-chat"
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # 你的投资经理人格设定
        self.system_prompt = """
        你是一位资深 A 股基金经理，专注于 300 亿市值以上的大盘低估值蓝筹股。
        你的风格是：稳健增长、1-2 周短中期波段操作。
        
        任务要求：
        1. 分析用户提供的股票代码，结合最新的行情和新闻。
        2. 给出深度逻辑分析（结论）。
        3. 提供精确的交易建议：理想买入价、止损位、止盈目标位。
        
        【强制输出格式】：
        你必须仅输出一个纯 JSON 对象，不要包含任何解释性文字或 Markdown 标签。
        JSON 结构如下：
        {
            "conclusion": "分析美的集团(000333)当前处于底部横盘，家电外销数据超预期...",
            "entry_price": "72.50",
            "stop_loss": "68.80",
            "target_price": "81.20"
        }
        """

    def run(self, user_prompt):
        """
        核心运行逻辑
        """
        logger.info(f"Agent 开始分析请求: {user_prompt[:50]}...")
        
        try:
            # 调用 DeepSeek API
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                api_key=self.api_key,
                temperature=0.3,  # 降低随机性，确保逻辑严密
                max_tokens=1000
            )

            # 提取模型返回的内容
            content = response.choices[0].message.content
            
            # 记录原始输出以便调试
            logger.debug(f"Agent Raw Output: {content}")
            
            # 返回给 main.py 处理（main.py 里已有正则清洗逻辑）
            return content

        except Exception as e:
            logger.error(f"DeepSeek 调用失败: {str(e)}")
            # 返回一个标准的错误 JSON 结构
            error_res = {
                "conclusion": "由于网络波动或 API 限制，AI 暂时无法完成深度扫描。",
                "entry_price": "--",
                "stop_loss": "--",
                "target_price": "--"
            }
            return json.dumps(error_res)

# 测试脚本 (当直接运行此文件时执行)
if __name__ == "__main__":
    agent = FinanceAgent()
    test_res = agent.run("分析 000333 美的集团，最近有家电补贴政策。")
    print(f"测试返回结果:\n{test_res}")