import os
import sys
import asyncio
import json
import re
import uvicorn
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File 
from fastapi.responses import HTMLResponse
# 动态修正路径，确保能找到 src 文件夹
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入自定义模块
from src.utils.agent_core import FinanceAgent 
from src.data.data_provider import get_stock_kline, get_stock_news, get_xueqiu_sentiment
from src.utils.logger import logger

app = FastAPI()
agent = FinanceAgent()

@app.get("/")
async def get():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # 将图片转为 Base64 供 AI 识别（假设你的 Agent 支持多模态）
        img_base64 = base64.b64encode(contents).decode('utf-8')
        
        prompt = "这是一张股票持仓截图，请识别其中的股票代码、成本价和盈亏情况，并给出简要诊断建议。请返回 JSON 格式。"
        # 这里调用 Agent 的识图方法
        analysis = agent.run_with_image(prompt, img_base64) 
        
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        logger.error(f"Image Analysis Error: {e}")
        return {"status": "error", "message": str(e)}

@app.websocket("/ws/analyze")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Terminal WebSocket Connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            code = request.get("code")
            if not code: continue

            # 1. 状态更新
            await websocket.send_json({"type": "status", "message": f"正在穿透网关获取 {code}..."})
            
            # 2. 获取数据 (优先行情)
            kline = get_stock_kline(code)
            news = get_stock_news(code)
            sentiment = get_xueqiu_sentiment(code)

            # 3. 🚀 关键：立即推送到前端绘图，不等待 AI
            if kline:
                await websocket.send_json({"type": "kline", "data": kline})
            if news:
                await websocket.send_json({"type": "news", "data": news})
            
            await websocket.send_json({"type": "status", "message": "行情已就绪，AI 经理正在复盘..."})

            # 4. 异步调用 AI Agent
            try:
                # 构造 Prompt，包含最新价格
                last_close = kline[-1]['close'] if kline else "未知"
                news_context = "\n".join([n['title'] for n in news[:3]])
                prompt = f"分析股票 {code}。最新价: {last_close}。近期动态: {news_context}。请按 JSON 格式给出建议。"
                
                loop = asyncio.get_event_loop()
                raw_ai_res = await loop.run_in_executor(None, agent.run, prompt)
                
                # 正则清洗并提取 JSON
                match = re.search(r'\{.*\}', raw_ai_res, re.DOTALL)
                if match:
                    # 移除换行符防止解析失败
                    clean_json = match.group(0).replace('\n', '').replace('\r', '')
                    ai_json = json.loads(clean_json)
                    await websocket.send_json({
                        "type": "result", 
                        "payload": ai_json, 
                        "sentiment": sentiment
                    })
                else:
                    await websocket.send_json({"type": "status", "message": "AI 结论生成异常"})
            except Exception as e:
                logger.error(f"AI Agent Error: {e}")
                await websocket.send_json({"type": "status", "message": "AI 暂时离线"})

    except WebSocketDisconnect:
        logger.info("Terminal Disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)