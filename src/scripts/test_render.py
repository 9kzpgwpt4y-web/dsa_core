from src.utils.renderer import ReportRenderer
from src.utils.logger import logger

def main():
    # 1. 模拟底层行情和估值数据
    stock_info = {
        "name": "平安银行",
        "code": "000001",
        "market_cap": 2045.6,
        "pe": 5.2,
        "pb": 0.65,
        "trend": "多头排列 (MA5 > MA20)"
    }

    # 2. 模拟昨天 DeepSeek 吐出来的标准 JSON 结果
    mock_ai_output = {
        "conclusion": "当前估值处于历史低位，技术面呈现多头排列，安全边际较高，建议逢低布局参与波段轮动。",
        "entry_price": "10.20 - 10.50",
        "stop_loss": "9.80 (跌破前期支撑位)",
        "target_price": "11.50 (上方半年线压力位)",
        "risks": [
            "宏观经济复苏不及预期，导致信贷需求疲软",
            "大盘整体出现系统性回调风险",
            "短期内成交量未见明显放大，可能存在诱多"
        ]
    }

    # 3. 渲染出图
    logger.info("正在将数据渲染为 Markdown 报告...")
    renderer = ReportRenderer()
    final_markdown = renderer.render(mock_ai_output, stock_info)
    
    # 打印结果
    print("\n" + "="*50)
    print(final_markdown)
    print("="*50 + "\n")
    logger.success("报告渲染测试完成！")

if __name__ == "__main__":
    main()