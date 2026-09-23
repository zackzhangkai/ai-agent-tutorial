"""
文件名：src/03_openai_tool_calling.py
说明：标准 OpenAI 协议 Tool Calling 原生 5 步闭环可运行实现
运行方式：uv run python src/03_openai_tool_calling.py
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

# 1. 本地真实业务函数
def refund_order_api(order_id: str, reason: str) -> dict:
    """真实 ERP 退款发起接口"""
    print(f"\n[真实系统执行] 正在处理退款: 订单号={order_id}, 退款原因={reason}")
    return {
        "status": "success",
        "order_id": order_id,
        "refund_amount": 299.00,
        "refund_ticket_id": "RF20260923001",
        "notice": "退款申请已受理，预计 1-3 个工作日退回原支付账户。"
    }

def query_order_logistics(order_id: str) -> dict:
    """真实 ERP 物流查询接口"""
    print(f"\n[真实系统执行] 正在查询物流: 订单号={order_id}")
    return {
        "status": "in_transit",
        "order_id": order_id,
        "carrier": "顺丰特快",
        "current_hub": "华东中心转运站",
        "eta": "今天 18:00 前"
    }

# 2. 工具元数据规约 (符合 JSON Schema 规范)
TOOLS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "refund_order_api",
            "description": "当用户明确要求对指定订单发起退款时调用本接口",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "8位数字订单流水号，例如 20260901"
                    },
                    "reason": {
                        "type": "string",
                        "description": "用户陈述的退款具体原因，例如：尺码不合、质量问题、误购"
                    }
                },
                "required": ["order_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_order_logistics",
            "description": "当用户想知道订单的物流进度、当前位置或预计送达时间时调用本接口",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "8位数字订单流水号，例如 20260901"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]

FUNCTION_MAP = {
    "refund_order_api": refund_order_api,
    "query_order_logistics": query_order_logistics
}

def run_tool_calling_flow(user_input: str):
    print(f"\n==========================================")
    print(f"--- [收到用户输入] {user_input} ---")
    messages = [
        {
            "role": "system",
            "content": "你是一家品牌官方旗舰店的售后 AI Agent。如果用户要求退款或查物流且提供了订单号，请准确调用对应的后台接口。"
        },
        {"role": "user", "content": user_input}
    ]

    # 第 1 步：大模型分析并输出工具调用指令
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS_CONFIG,
        tool_choice="auto"
    )
    msg = response.choices[0].message
    messages.append(msg)

    # 第 2 步：判断是否产生 tool_calls
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            print(f"👉 模型识别需要调用: {func_name}，解析出参数: {func_args}")

            # 第 3 步：本地调度执行真实函数
            func = FUNCTION_MAP.get(func_name)
            if func:
                result = func(**func_args)
            else:
                result = {"error": f"未定义工具 {func_name}"}

            # 第 4 步：回传 tool 观察结果
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": json.dumps(result, ensure_ascii=False)
            })

        # 第 5 步：模型基于真实业务数据生成最终礼貌回复
        final_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final_resp.choices[0].message.content
    else:
        return msg.content

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("💡 演示说明：配置 OPENAI_API_KEY 后即可运行真实的 GPT-4o 5步工具调用闭环！")
    else:
        ans1 = run_tool_calling_flow("你好，我的订单 20260901 衣服买大了一号，帮我申请全额退款。")
        print("\n[最终答复]:\n", ans1)
        
        ans2 = run_tool_calling_flow("帮我查一下订单 20260901 到哪里了？今天能到吗？")
        print("\n[最终答复]:\n", ans2)
