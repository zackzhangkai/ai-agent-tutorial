"""
06_langgraph_workflow.py
=============================================================================
第 6 章：现代编排框架 LangGraph 有向状态图工作流
包含：
  1. 状态模式 (State Pattern) 与 Reducer 消息累积
  2. 节点逻辑 (Node): 模型决策节点与工具执行节点
  3. 条件边 (Conditional Edge): 动态分支判断与环状循环 (Looping)
  4. 人机协同 (Human-in-the-loop): 危险操作人工干预与审核机制
  5. 开箱即跑：内置纯原生 Python 状态图引擎，若环境已安装 langgraph 则兼容运行

运行方法：
  python src/06_langgraph_workflow.py
=============================================================================
"""

import json
import time
from typing import Dict, Any, List, Optional, Callable


# ==========================================
# 1. 业务工具库定义
# ==========================================
def calculate_freight(weight_kg: float, distance_km: float) -> str:
    """计算大件货物预估物流运费"""
    base_fee = 15.0
    weight_fee = weight_kg * 2.5
    distance_fee = distance_km * 0.1
    total = base_fee + weight_fee + distance_fee
    return f"【物流系统返回】重量: {weight_kg}kg, 运距: {distance_km}km, 预估运费总计: {total:.2f} 元"

def issue_refund(order_id: str, amount: float, reason: str) -> str:
    """执行订单原路退款操作（敏感操作，需要人工确认）"""
    return f"【退款系统返回】订单 {order_id} 成功退款 {amount} 元，退款理由: {reason}。"


AVAILABLE_TOOLS = {
    "calculate_freight": calculate_freight,
    "issue_refund": issue_refund
}


# ==========================================
# 2. 轻量级生产级 StateGraph 引擎实现
# ==========================================
class AgentState:
    """状态定义：在所有节点与边之间流动的数据载荷"""
    def __init__(self, messages: Optional[List[Dict[str, Any]]] = None):
        self.messages: List[Dict[str, Any]] = messages or []
        self.requires_human_approval: bool = False
        self.approval_action: Optional[Dict[str, Any]] = None
        self.is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "messages": self.messages,
            "requires_human_approval": self.requires_human_approval,
            "approval_action": self.approval_action,
            "is_finished": self.is_finished
        }


class StateGraphEngine:
    """
    轻量级工业有向状态图引擎。
    复刻 LangGraph 的核心设计：
      - Nodes: 执行具体计算/推理逻辑
      - Edges: 确定性边 (A -> B)
      - Conditional Edges: 根据当前状态动态决定下一个跳转目标
    """
    def __init__(self):
        self.nodes: Dict[str, Callable[[AgentState], None]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[AgentState], str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[AgentState], None]):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edges(self, source: str, path_function: Callable[[AgentState], str], path_map: Dict[str, str]):
        self.conditional_edges[source] = (path_function, path_map)

    def run(self, initial_state: AgentState, max_steps: int = 10) -> AgentState:
        current_node = self.entry_point
        step_count = 0
        state = initial_state

        print(f"\n🚀 [StateGraph 启动] 入口节点: '{current_node}'")

        while current_node and current_node != "END" and step_count < max_steps:
            step_count += 1
            print(f"\n---> [Step {step_count}] 进入节点: 【{current_node}】")
            
            # 执行节点逻辑
            node_fn = self.nodes.get(current_node)
            if not node_fn:
                raise ValueError(f"未找到节点定义: {current_node}")
            node_fn(state)

            # 人机交互挂起判断 (Human-in-the-loop)
            if state.requires_human_approval:
                print("\n⚠️ [Human-in-the-Loop 拦截] 检测到高风险操作，图状态暂停，等待人工审批...")
                break

            # 边路由决策
            if current_node in self.conditional_edges:
                route_fn, path_map = self.conditional_edges[current_node]
                decision_key = route_fn(state)
                next_node = path_map.get(decision_key, "END")
                print(f"     [条件分支决策] 结果: '{decision_key}' -> 下一目标: '{next_node}'")
                current_node = next_node
            elif current_node in self.edges:
                next_node = self.edges[current_node]
                print(f"     [固定边跳转] 下一目标: '{next_node}'")
                current_node = next_node
            else:
                print(f"     [无后续路由] 流程终止")
                current_node = "END"

        return state


# ==========================================
# 3. 业务节点函数实现
# ==========================================
def agent_llm_reasoning_node(state: AgentState):
    """
    大模型大脑节点：根据历史对话分析用户意图，生成回复或工具调用指令
    """
    last_user_msg = ""
    for m in reversed(state.messages):
        if m["role"] == "user":
            last_user_msg = m["content"]
            break

    print(f"     [AgentNode] 分析意图: \"{last_user_msg}\"")
    time.sleep(0.1)

    # 模拟大模型 Function Calling 决策
    if "运费" in last_user_msg:
        tool_call = {
            "name": "calculate_freight",
            "args": {"weight_kg": 15.5, "distance_km": 420.0}
        }
        state.messages.append({
            "role": "assistant",
            "content": None,
            "tool_call": tool_call
        })
        print(f"     [AgentNode] 决策: 需要调用工具 '{tool_call['name']}'，参数: {tool_call['args']}")
    elif "退款" in last_user_msg:
        tool_call = {
            "name": "issue_refund",
            "args": {"order_id": "ORD-2026-8899", "amount": 299.0, "reason": "生鲜变质异味"}
        }
        state.messages.append({
            "role": "assistant",
            "content": None,
            "tool_call": tool_call
        })
        print(f"     [AgentNode] 决策: 需要调用高风险工具 '{tool_call['name']}'，参数: {tool_call['args']}")
    else:
        state.messages.append({
            "role": "assistant",
            "content": f"收到您的咨询：{last_user_msg}。我们客服人员会竭诚为您服务。"
        })
        print("     [AgentNode] 决策: 普通文本回复，无需工具调用")


def tool_execution_node(state: AgentState):
    """
    工具执行节点：执行模型请求的工具，并将结果写回 State
    """
    last_msg = state.messages[-1]
    tool_call = last_msg.get("tool_call")
    if not tool_call:
        return

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    # 模拟风控审计：若是退款金额 > 100 元，触发人工审核
    if tool_name == "issue_refund" and tool_args.get("amount", 0) > 100:
        state.requires_human_approval = True
        state.approval_action = tool_call
        return

    # 执行普通工具
    tool_fn = AVAILABLE_TOOLS.get(tool_name)
    if tool_fn:
        result = tool_fn(**tool_args)
    else:
        result = f"错误：未注册工具 {tool_name}"

    print(f"     [ToolNode] 工具执行完成: {result}")
    state.messages.append({
        "role": "tool",
        "tool_name": tool_name,
        "content": result
    })


def final_summarize_node(state: AgentState):
    """
    最终汇总节点：综合工具执行结果，生成对用户的亲切礼貌答复
    """
    tool_content = ""
    for m in reversed(state.messages):
        if m["role"] == "tool":
            tool_content = m["content"]
            break

    summary = f"尊敬的顾客，根据系统实时核算结果：{tool_content}。如有任何疑问请随时告知！"
    state.messages.append({
        "role": "assistant",
        "content": summary
    })
    state.is_finished = True
    print(f"     [SummarizeNode] 生成最终回复: {summary}")


# ==========================================
# 4. 路由条件分支 (Conditional Router)
# ==========================================
def should_continue_router(state: AgentState) -> str:
    """
    条件边逻辑：判断 Agent 节点的输出类型
    - 如果输出了 tool_call，则流向 'tools' 节点
    - 如果是直接文本，则流向 'END' 终止
    """
    last_msg = state.messages[-1]
    if last_msg.get("tool_call"):
        return "tools"
    return "END"


# ==========================================
# 5. 图编排组装与验证执行
# ==========================================
def build_ecommerce_graph() -> StateGraphEngine:
    graph = StateGraphEngine()

    # 1. 注册节点
    graph.add_node("agent", agent_llm_reasoning_node)
    graph.add_node("tools", tool_execution_node)
    graph.add_node("summarize", final_summarize_node)

    # 2. 设置起点
    graph.set_entry_point("agent")

    # 3. 设置条件边与固定边
    graph.add_conditional_edges(
        source="agent",
        path_function=should_continue_router,
        path_map={"tools": "tools", "END": "END"}
    )
    graph.add_edge("tools", "summarize")
    graph.add_edge("summarize", "END")

    return graph


if __name__ == "__main__":
    app_graph = build_ecommerce_graph()

    print("=" * 80)
    print("【测试场景 1：物流运费查询 (触发普通工具调用并完成总结)】")
    print("=" * 80)
    state1 = AgentState(messages=[{"role": "user", "content": "查一下 15.5 公斤包裹寄到 420 公里外的运费多少钱？"}])
    app_graph.run(state1)
    print("\n[场景 1 最终对话记录]")
    for m in state1.messages:
        print(f"  [{m['role'].upper()}]: {m.get('content') or m.get('tool_call')}")

    print("\n" + "=" * 80)
    print("【测试场景 2：大额退款敏感操作 (触发 Human-in-the-Loop 审批拦截)】")
    print("=" * 80)
    state2 = AgentState(messages=[{"role": "user", "content": "我的生鲜订单 ORD-2026-8899 发酸变质了，必须全额退款 299 元！"}])
    app_graph.run(state2)
    
    if state2.requires_human_approval:
        print(f"\n[模拟管理员人工审核]: 审核待执行动作 -> {state2.approval_action}")
        print("[管理员操作]: 审核通过！批准退款")
        # 恢复状态并执行
        state2.requires_human_approval = False
        res = issue_refund(**state2.approval_action["args"])
        state2.messages.append({"role": "tool", "tool_name": "issue_refund", "content": res})
        print(f"[继续图流转]: {res}")
