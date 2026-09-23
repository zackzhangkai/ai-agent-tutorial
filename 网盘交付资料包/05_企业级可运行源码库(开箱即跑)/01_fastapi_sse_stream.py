"""
文件名：src/01_fastapi_sse_stream.py
说明：生产级 FastAPI + SSE (Server-Sent Events) 打字机流式服务标准实现
运行方式：uv run uvicorn src.01_fastapi_sse_stream:app --reload --port 8000
测试方式：curl -N "http://127.0.0.1:8000/api/v1/agent/chat?query=我的订单20260901到哪了"
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import json
from datetime import datetime

app = FastAPI(
    title="AI Agent Production Streaming Service",
    description="支持思考轨迹追踪与实时自然语言打字机的标准接口",
    version="1.0.0"
)

# 生产环境跨域安全配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请指定具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def agent_execution_generator(user_query: str):
    """
    模拟 Agent 完整的思考、工具调用与答案生成全链路事件流
    """
    # 阶段 1：接收并解析意图
    stage_1 = {
        "event_id": 1,
        "type": "thought",
        "stage": "intent_parsing",
        "timestamp": datetime.now().isoformat(),
        "message": f"正在深度分析用户需求：'{user_query}'，识别到包含查单与政策咨询双重意图..."
    }
    yield f"data: {json.dumps(stage_1, ensure_ascii=False)}\n\n"
    await asyncio.sleep(0.6)

    # 阶段 2：规划并调用工具
    stage_2 = {
        "event_id": 2,
        "type": "tool_call",
        "stage": "action_execution",
        "tool_name": "query_order_status",
        "arguments": {"order_id": "20260901"},
        "message": "正在请求内部 ERP 接口查询订单 [20260901] 的最新物流动态..."
    }
    yield f"data: {json.dumps(stage_2, ensure_ascii=False)}\n\n"
    await asyncio.sleep(0.8)

    # 阶段 3：观察外部返回
    stage_3 = {
        "event_id": 3,
        "type": "observation",
        "stage": "data_received",
        "result": {"status": "运输中", "hub": "华东中心转运站", "courier": "顺丰特快"},
        "message": "接口返回成功：包裹正处于顺丰特快陆运中，预计今日 18:00 送达。"
    }
    yield f"data: {json.dumps(stage_3, ensure_ascii=False)}\n\n"
    await asyncio.sleep(0.5)

    # 阶段 4：自然语言打字机流式输出最终答复
    final_answer = (
        "您好！为您查询到订单号 20260901 的最新进展如下：\n\n"
        "1. 物流承运：顺丰特快\n"
        "2. 当前位置：已到达【华东中心转运站】，正在进行分拣派发\n"
        "3. 预计送达：今天下午 18:00 前完成送货上门\n\n"
        "请您保持手机畅通，如有其他疑问可随时告诉我！"
    )
    
    # 逐字拆包打字机推送
    for char in final_answer:
        chunk = {
            "type": "answer_chunk",
            "content": char
        }
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.03)  # 模拟自然的打字手感

    # 结束标志
    yield f"data: {json.dumps({'type': 'done'})}\n\n"

@app.get("/api/v1/agent/chat")
async def chat_stream_endpoint(query: str = Query(..., description="用户的提问内容")):
    """
    对外暴露的标准 SSE 流式通信端点
    """
    return StreamingResponse(
        agent_execution_generator(query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 关键：通知 Nginx/网关不要对流式内容进行缓冲
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.01_fastapi_sse_stream:app", host="127.0.0.1", port=8000, reload=True)
