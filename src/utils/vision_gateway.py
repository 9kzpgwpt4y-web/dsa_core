import base64
from litellm import completion

class VisionGateway:
    def __init__(self, model="deepseek/deepseek-chat"):
        self.model = model

    def extract_stock_from_image(self, image_path: str):
        # 将图片转为 Base64
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')

        prompt = "这是一张股票账户持仓截图。请提取所有的股票名称和对应的 6 位股票代码，并以 JSON 格式输出，例如：[{'name': '平安银行', 'code': '000001'}]"

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content