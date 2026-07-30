import os
import yaml
from litellm import completion
from src.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

class LLMGateway:
    def __init__(self):
        with open("config/models.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        self.default_model = self.config.get("default_model")

    def ask(self, system_prompt: str, user_prompt: str, model=None):
        """
        同步调用（方便目前调试）
        """
        target_model = model or self.default_model
        try:
            logger.info(f"正在调用模型: {target_model}")
            response = completion(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.get("temperature", 0.2),
                response_format={ "type": "json_object" } # 强制要求 JSON 格式输出
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return None