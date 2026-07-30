import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from src.utils.logger import logger

class ReportRenderer:
    def __init__(self, template_dir="templates"):
        # 1. 获取项目根目录的绝对路径
        current_dir = os.getcwd()
        template_path = os.path.join(current_dir, template_dir)
        
        # 2. 检查模板文件夹是否存在
        if not os.path.exists(template_path):
            logger.error(f"找不到模板文件夹: {template_path}")
            raise FileNotFoundError(f"目录不存在: {template_path}")

        # 3. 【关键修复】显式指定 encoding='utf-8'，防止 Windows 下乱码报错
        self.env = Environment(loader=FileSystemLoader(template_path, encoding='utf-8'))
        
        try:
            self.template = self.env.get_template("report.md")
        except Exception as e:
            logger.error(f"加载模板失败: {str(e)}")
            raise e

    def render(self, ai_json_data: dict, stock_info: dict) -> str:
        """
        将基础信息和 AI 返回的 JSON 字典合并渲染为 Markdown
        """
        try:
            context = {
                "stock_name": stock_info.get("name", "未知名称"),
                "stock_code": stock_info.get("code", "未知代码"),
                "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "market_cap": stock_info.get("market_cap", "N/A"),
                "pe_ratio": stock_info.get("pe", "N/A"),
                "pb_ratio": stock_info.get("pb", "N/A"),
                "trend_status": stock_info.get("trend", "震荡"),
                **ai_json_data 
            }
            return self.template.render(context)
        except Exception as e:
            logger.error(f"渲染过程出错: {str(e)}")
            return f"渲染失败: {str(e)}"