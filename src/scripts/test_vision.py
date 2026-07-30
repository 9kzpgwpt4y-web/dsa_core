import os
from src.utils.vision_gateway import VisionGateway
from src.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

def main():
    # 指向你刚才放图片的路径
    image_path = "screenshots/portfolio.png"
    
    if not os.path.exists(image_path):
        logger.error(f"❌ 找不到图片文件: {image_path}")
        return

    logger.info("正在唤醒 AI 眼睛进行视觉分析...")
    
    vg = VisionGateway(model="deepseek/deepseek-chat")
    
    try:
        result = vg.extract_stock_from_image(image_path)
        print("\n" + "🔍" + " 识别结果 " + "🔍")
        print("="*30)
        print(result)
        print("="*30)
        logger.success("视觉提取成功！")
    except Exception as e:
        logger.error(f"视觉分析失败: {e}")

if __name__ == "__main__":
    main()