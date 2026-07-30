import os
import json
from datetime import datetime
from dotenv import load_dotenv

from src.utils.agent_core import CryptoAgent  # 之前 Day4 写的 Agent
from src.utils.renderer import ReportRenderer
from src.utils.logger import logger

# 强制加载环境变量（GitHub Actions 环境下也可以读取 Secrets）
load_dotenv()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_watchlist():
    """获取要分析的股票池，如果本地没有配置文件，就默认提供几个符合大盘价值特征的标的"""
    watchlist_path = "config/watchlist.json"
    if os.path.exists(watchlist_path):
        with open(watchlist_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # 默认兜底的大盘股测试池（市值>300亿，低估值）
    return [
        {"code": "000001", "name": "平安银行"},
        {"code": "601318", "name": "中国平安"}
    ]

def main():
    logger.info("🚀 启动每日自动化量化投研流水线...")
    
    # 1. 初始化目录和组件
    ensure_dir("reports")
    watchlist = get_watchlist()
    agent = CryptoAgent()
    renderer = ReportRenderer()
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 2. 遍历自选股池进行深度分析
    for stock in watchlist:
        stock_name = stock['name']
        stock_code = stock['code']
        logger.info(f"👉 正在分析: {stock_name} ({stock_code})")
        
        # 构造带有强烈风格约束的提示词
        prompt = f"""
        请调用你的工具获取 {stock_name}({stock_code}) 的最新行情和技术指标。
        
        作为一名资深基金经理，请你严格执行以下投资纪律进行分析：
        1. 必须排查该股总市值是否在300亿-400亿人民币以上，以及当前的PE/PB估值是否处于低位安全区。
        2. 结合基本面与当前多空趋势，制定一个持股周期为 1-2 周的波段轮动计划。
        3. 坚决回避极端高位股，以稳健为主，设定明确的防守底线。
        
        请务必按照以下 JSON 格式输出最终结论，不要输出额外的解释文本：
        {{
            "conclusion": "核心结论，评估是否满足大盘低估值标准及当前操作建议",
            "entry_price": "建议的入场区间",
            "stop_loss": "明确的止损点位",
            "target_price": "1-2周内的止盈目标位",
            "risks": ["风险1", "风险2"]
        }}
        """
        
        try:
            # 唤醒 Agent 进行多轮工具调用与思考
            raw_response = agent.run(prompt)
            
            # 清理模型可能返回的 Markdown 标记（如 ```json ... ```）
            clean_json_str = raw_response.replace("```json", "").replace("```", "").strip()
            ai_data = json.loads(clean_json_str)
            
            # 模拟合并底层基础数据（实际工程中由 DataProvider 提供）
            stock_info = {
                "name": stock_name,
                "code": stock_code,
                "market_cap": "待工具补充", 
                "pe": "待工具补充",
                "pb": "待工具补充",
                "trend": "分析完毕"
            }
            
            # 3. 渲染为精美的 Markdown 研报
            final_report = renderer.render(ai_data, stock_info)
            
            # 4. 保存报告到本地
            report_filename = f"reports/{today_str}_{stock_name}.md"
            with open(report_filename, "w", encoding="utf-8") as f:
                f.write(final_report)
                
            logger.success(f"✅ {stock_name} 分析完成，报告已生成: {report_filename}")
            
            # TODO: 这里可以接入昨天讨论的 Webhook 企业微信推送 或 PyXLL 写入
            
        except Exception as e:
            logger.error(f"❌ 分析 {stock_name} 时发生异常: {e}")
            continue

    logger.info("🎉 今日所有自选股分析任务已全部执行完毕！")

if __name__ == "__main__":
    main()