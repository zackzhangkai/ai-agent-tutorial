"""
文件名：src/02_native_react_engine.py
说明：纯原生 Python 手写实现工业级 ReAct (Reason + Act) 规划循环引擎
运行方式：uv run python src/02_native_react_engine.py
"""

import os
import json
from typing import Callable, Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

# ----------------- 1. 定义真实外部业务工具 -----------------
def get_current_weather(location: str) -> Dict[str, Any]:
    """模拟查询指定城市实时天气的工具"""
    fake_weather_db = {
        "北京": {"temp": "24°C", "condition": "晴朗", "humidity": "45%"},
        "上海": {"temp": "28°C", "condition": "大雨", "humidity": "85%"},
        "深圳": {"temp": "31°C", "condition": "多云", "humidity": "70%"}
    }
    return fake_weather_db.get(location, {"temp": "22°C", "condition": "多云", "humidity": "50%"})

def calculate_ticket_price(origin: str, destination: str, is_high_speed: bool = True) -> Dict[str, Any]:
    """模拟计算两地之间火车票价的工具"""
    return {
        "route": f"{origin} -> {destination}",
        "type": "高铁二等座" if is_high_speed else "普通卧铺",
        "price_rmb": 553.0 if is_high_speed else 280.0,
        "available_seats": 12
    }

# ----------------- 2. 工具元数据注册表 (Tools Schema) -----------------
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的实时天气、气温与湿度信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市中文名称，例如：北京、上海、深圳"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_ticket_price",
            "description": "查询两个城市之间火车票票价与余票情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "出发城市"},
                    "destination": {"type": "string", "description": "到达城市"},
                    "is_high_speed": {"type": "boolean", "description": "是否为高铁动车，默认为 True"}
                },
                "required": ["origin", "destination"]
            }
        }
    }
]

# 本地可执行函数映射字典
FUNCTION_MAP: Dict[str, Callable] = {
    "get_current_weather": get_current_weather,
    "calculate_ticket_price": calculate_ticket_price
}

# ----------------- 3. 原生 ReAct 核心引擎实现 -----------------
def execute_react_agent(user_prompt: str, max_iterations: int = 5) -> str:
    """
    原生实现的 ReAct 运行循环
    :param user_prompt: 用户的初始任务描述
    :param max_iterations: 最大安全循环次数，防止死循环
    """
    print(f"\n🚀 [Agent 任务启动] 用户目标: {user_prompt}")
    
    # 初始化会话上下文与专业系统提示词
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "你是一个严谨务实的旅行与出行助手 AI Agent。\n"
                "当你面对用户目标时，请遵循 ReAct 决策模式：\n"
                "1. 在调用工具前，明确你的思考目标 (Thought)；\n"
                "2. 根据真实需要选择调用最合适的工具 (Action)；\n"
                "3. 基于工具返回的事实数据进行下一步推理 (Observation)；\n"
                "4. 最终以结构清晰、友善的自然语言给出最终答复 (Final Answer)。"
            )
        },
        {"role": "user", "content": user_prompt}
    ]

    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- [第 {iteration} 轮迭代推理] ---")

        # 触发大模型推理
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)

        # 判断模型是否决定调用工具
        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                
                print(f"👉 [Agent Action] 决定调用工具: {func_name}")
                print(f"   参数内容: {func_args}")

                # 本地执行对应 Python 函数
                target_func = FUNCTION_MAP.get(func_name)
                if target_func:
                    tool_output = target_func(**func_args)
                else:
                    tool_output = {"error": f"工具 {func_name} 未在本地注册"}

                print(f"👁️ [Agent Observation] 工具返回数据: {tool_output}")

                # 将工具执行结果作为 role: tool 追加至上下文
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": json.dumps(tool_output, ensure_ascii=False)
                })
        else:
            # 没有触发工具调用，说明 Agent 已经得出最终结论
            print(f"\n✅ [任务顺利闭环] Agent 生成最终答复：")
            return message.content

    return "⚠️ 警告：Agent 达到最大推理迭代限制，为保障安全已终止执行并转人工审核。"

# ----------------- 4. 本地测试运行 -----------------
if __name__ == "__main__":
    test_query = "我想明天从北京去上海出差，帮我看下上海现在的天气适不适合出行，另外算一下高铁二等座票价大概多少钱？"
    if os.getenv("OPENAI_API_KEY") in [None, "", "your-api-key-here"]:
        print("💡 提示：请在 .env 文件中配置真实的 OPENAI_API_KEY 即可实际执行大模型推理测试！")
        print("（本地模拟环境展示结束）")
    else:
        final_result = execute_react_agent(test_query)
        print(final_result)
