from src.utils.agent_core import CryptoAgent
from src.utils.logger import logger

def main():
    agent = CryptoAgent()
    print("--- 🤖 A股量化 Agent 已上线 (输入 'exit' 退出) ---")
    
    while True:
        user_input = input("\n👤 你: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        logger.info("Agent 正在思考...")
        response = agent.run(user_input)
        print(f"\n🤖 Agent: {response}")

if __name__ == "__main__":
    main()