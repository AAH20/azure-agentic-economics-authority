from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


@dataclass
class EconomicsTraceHandler:
    """LangChain-compatible callback surface without a hard LangChain dependency."""
    workflow: str
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    node_durations_ms: dict[str, float] = field(default_factory=dict)
    _starts: dict[str, float] = field(default_factory=dict)

    def on_chain_start(self, serialized: dict[str, Any], inputs: dict[str, Any], *, run_id: Any, **_: Any) -> None:
        self._starts[str(run_id)] = perf_counter()

    def on_chain_end(self, outputs: dict[str, Any], *, run_id: Any, **_: Any) -> None:
        start = self._starts.pop(str(run_id), None)
        if start is not None:
            name = str(outputs.get("node", run_id))
            self.node_durations_ms[name] = (perf_counter() - start) * 1000

    def on_llm_end(self, response: Any, **_: Any) -> None:
        usage = getattr(response, "llm_output", {}) or {}
        token_usage = usage.get("token_usage", usage.get("usage", {}))
        self.input_tokens += int(token_usage.get("prompt_tokens", token_usage.get("input_tokens", 0)))
        self.output_tokens += int(token_usage.get("completion_tokens", token_usage.get("output_tokens", 0)))

    def on_tool_start(self, serialized: dict[str, Any], input_str: str, **_: Any) -> None:
        self.tool_calls += 1

    def receipt(self) -> dict[str, Any]:
        return {
            "workflow": self.workflow,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "tool_calls": self.tool_calls,
            "node_durations_ms": self.node_durations_ms,
        }

