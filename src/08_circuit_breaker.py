"""
08_circuit_breaker.py
=============================================================================
第 8 章：生产级 Agent 防死循环熔断器与高可用安全网关 (Circuit Breaker)
包含：
  1. 状态滑动窗口追踪 (Sliding Window Tracker)
  2. 连续重复调用熔断 (Duplicate Invocation Breaker)
  3. 全局迭代步数熔断 (Max Iterations Breaker)
  4. 参数震荡死锁检测 (Oscillating Deadlock Detector)
  5. 自动降级与兜底策略 (Fallback & Graceful Degradation)

运行方法：
  python src/08_circuit_breaker.py
=============================================================================
"""

import time
import json
from typing import Dict, Any, List, Optional, Tuple


class AgentCircuitBreakerException(Exception):
    """Agent 熔断器异常基类"""
    pass

class MaxIterationExceededError(AgentCircuitBreakerException):
    """超过全局最大迭代步数"""
    pass

class DuplicateCallLoopError(AgentCircuitBreakerException):
    """检测到相同工具与参数的死循环"""
    pass

class PingPongOscillationError(AgentCircuitBreakerException):
    """检测到两工具之间的乒乓震荡死循环"""
    pass


class AgentCircuitBreaker:
    """
    生产级智能体运行时熔断保护控制器。
    部署在 Agent 核心循环中，每一次 LLM 决策触发工具前进行拦截校验。
    """
    def __init__(
        self,
        max_total_steps: int = 6,
        max_consecutive_same_tool: int = 2,
        enable_param_hash_check: bool = True
    ):
        self.max_total_steps = max_total_steps
        self.max_consecutive_same_tool = max_consecutive_same_tool
        self.enable_param_hash_check = enable_param_hash_check
        self.call_history: List[Dict[str, Any]] = []

    def _hash_args(self, args: Dict[str, Any]) -> str:
        """对参数进行确定性哈希序列化"""
        return json.dumps(args, sort_keys=True, ensure_ascii=False)

    def record_and_verify(self, tool_name: str, tool_args: Dict[str, Any]) -> None:
        """
        在执行工具前调用。若检测到异常模式立即抛出熔断异常，中断执行。
        """
        step = len(self.call_history) + 1
        args_hash = self._hash_args(tool_args)
        current_record = {
            "step": step,
            "tool_name": tool_name,
            "args": tool_args,
            "args_hash": args_hash,
            "timestamp": time.time()
        }
        self.call_history.append(current_record)

        print(f"🛡️ [熔断器检查 Step {step}] 工具: '{tool_name}' | 参数: {tool_args}")

        # 规则 1: 全局总迭代步数熔断 (防止无限发散)
        if step > self.max_total_steps:
            raise MaxIterationExceededError(
                f"【熔断告警】已达到会话最大允许迭代步数上限 ({self.max_total_steps}步)，强制阻断。"
            )

        # 规则 2: 连续调用相同工具且参数完全一致 (最常见的自循环死锁)
        if len(self.call_history) >= self.max_consecutive_same_tool:
            recent_records = self.call_history[-self.max_consecutive_same_tool:]
            all_same_tool = all(r["tool_name"] == tool_name for r in recent_records)
            all_same_args = all(r["args_hash"] == args_hash for r in recent_records)

            if all_same_tool and all_same_args:
                raise DuplicateCallLoopError(
                    f"【熔断告警】检测到工具 '{tool_name}' 连续 {self.max_consecutive_same_tool} 次传入完全相同参数执行，智能体已陷入停滞死循环！"
                )

        # 规则 3: 乒乓震荡检测 (A -> B -> A -> B 交互震荡)
        if len(self.call_history) >= 4:
            c1, c2, c3, c4 = [r["tool_name"] for r in self.call_history[-4:]]
            if c1 == c3 and c2 == c4 and c1 != c2:
                raise PingPongOscillationError(
                    f"【熔断告警】检测到工具 '{c1}' 与 '{c2}' 形成乒乓交替死锁震荡链，强制中断！"
                )

        print("  -> 熔断器检查通过：状态健康。")

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_calls": len(self.call_history),
            "trace": [f"#{r['step']}: {r['tool_name']}" for r in self.call_history]
        }


# ==========================================
# 演示与模拟异常链路测试
# ==========================================
def simulate_bad_agent_execution():
    print("=" * 75)
    print("【测试场景 1：模拟 LLM 错误重试陷入同一工具相同参数死循环】")
    print("=" * 75)

    breaker = AgentCircuitBreaker(max_total_steps=8, max_consecutive_same_tool=2)
    
    # 模拟大模型连续尝试查询一个不存在的订单
    simulated_calls = [
        ("query_order", {"order_id": "NOT_EXIST_999"}),
        ("query_order", {"order_id": "NOT_EXIST_999"}),  # 第二次相同调用，应触发拦截
    ]

    for tool_name, args in simulated_calls:
        try:
            breaker.record_and_verify(tool_name, args)
            print("  --> 执行工具逻辑中...\n")
        except AgentCircuitBreakerException as e:
            print(f"\n🚨 {e}")
            print("  [优雅降级处理] 捕获死循环异常，自动转入客服兜底模版：")
            print("  \"抱歉，系统多次尝试查询未果，已为您自动转接值班技术工程师人工处理。\"\n")
            break

    print("=" * 75)
    print("【测试场景 2：模拟两工具之间乒乓震荡 (Tool_A <-> Tool_B)】")
    print("=" * 75)
    breaker_pingpong = AgentCircuitBreaker(max_total_steps=8)
    ping_pong_calls = [
        ("search_knowledge", {"query": "如何开具发票"}),
        ("query_tax_system", {"action": "check_invoice"}),
        ("search_knowledge", {"query": "如何开具发票"}),
        ("query_tax_system", {"action": "check_invoice"}),  # 形成 A-B-A-B 闭环
    ]

    for tool_name, args in ping_pong_calls:
        try:
            breaker_pingpong.record_and_verify(tool_name, args)
            print("  --> 执行工具逻辑中...\n")
        except AgentCircuitBreakerException as e:
            print(f"\n🚨 {e}")
            print("  [优雅降级处理] 捕获乒乓震荡，终止自动化图流转，保存 Checkpoint 快照。\n")
            break


if __name__ == "__main__":
    simulate_bad_agent_execution()
