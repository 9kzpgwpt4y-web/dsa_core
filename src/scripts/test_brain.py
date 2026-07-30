import pandas as pd
import json
import numpy as np
from src.data.analyzer import TechAnalyzer
from src.utils.llm_gateway import LLMGateway
from src.utils.prompts import QUANT_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.utils.logger import logger

def main():
    symbol, name = "000001", "平安银行"
    
    # --- 1. 构造模拟数据 (彻底绕过网络报错) ---
    logger.warning("检测到网络环境解析异常，正在切换至【模拟行情模式】以验证 AI 大脑...")
    
    # 生成 40 天的模拟价格（模拟一个上升趋势）
    base_price = 10.0
    dates = pd.date_range(start='2024-02-01', periods=40)
    # 模拟价格：10块钱底价 + 逐渐上涨 + 一点随机波动
    prices = [base_price + (i * 0.05) + np.random.normal(0, 0.1) for i in range(40)]
    
    data = {
        'open': prices,
        'high': [p + 0.1 for p in prices],
        'low': [p - 0.1 for p in prices],
        'close': prices,
        'volume': [100000] * 40
    }
    df = pd.DataFrame(data, index=dates)
    # ---------------------------------------

    # 2. 计算量化指标 (MA5, MA10, BIAS等)
    df_with_indicators = TechAnalyzer.calculate_indicators(df)
    last_row = df_with_indicators.iloc[-1]

    # 3. 构造喂给 AI 的情报包
    user_content = USER_PROMPT_TEMPLATE.format(
        name=name, 
        symbol=symbol,
        close=round(last_row['close'], 2),
        ma5=round(last_row['ma5'], 2),
        ma10=round(last_row['ma10'], 2),
        ma20=round(last_row['ma20'], 2),
        bias_5=round(last_row['bias_5'], 2),
        trend_status="多头排列（MA5 > MA10 > MA20）" if last_row['ma5'] > last_row['ma20'] else "横盘整理",
        news="平安银行近期发布业绩快报，净利润稳定增长，分红派息计划超预期，获得机构增持。"
    )

    # 4. 激活 LLM 决策大脑
    brain = LLMGateway()
    logger.info("正在发送情报包至DS...")
    raw_result = brain.ask(QUANT_SYSTEM_PROMPT, user_content)

    # 5. 输出结果
    if raw_result:
        try:
            # 尝试解析输出的 JSON
            # 有时模型会返回带有 ```json ... ``` 标签的文本，这里做个简单清洗
            clean_json = raw_result.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json)
            
            logger.success("✅ AI 决策大脑分析完成！")
            print("\n" + "="*50)
            print(json.dumps(result, indent=4, ensure_ascii=False))
            print("="*50 + "\n")
        except Exception as e:
            logger.error(f"解析 AI 返回结果失败: {e}")
            print("原始输出内容：", raw_result)

if __name__ == "__main__":
    main()