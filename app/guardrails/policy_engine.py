from dataclasses import dataclass


@dataclass
class PolicyResult:
    """@dataclass chosen over TypedDict for dot-access (.passed) — not used in LangGraph so no dict requirement."""
    passed: bool
    reason: str = ""

    # Allows tuple unpacking: passed, reason = PolicyResult(...)
    def __iter__(self):
        return iter((self.passed, self.reason))


class PolicyEngine:
    def validate_input(self, message: str) -> PolicyResult:
        suspicious_patterns = [
            "ignore previous instructions",
            "system prompt",
            "developer message",
        ]

        text = message.lower()

        for pattern in suspicious_patterns:
            if pattern in text:
                return PolicyResult(
                    passed=False,
                    reason=f"Matched pattern: {pattern}",
                )

        return PolicyResult(passed=True)

    def authorize_tool(self, tool_name: str) -> PolicyResult:
        allowed_tools = {"calculator", "weather"}

        if tool_name not in allowed_tools:
            return PolicyResult(
                passed=False,
                reason=f"{tool_name} is not authorized.",
            )

        return PolicyResult(passed=True)

    def validate_output(self, text: str) -> PolicyResult:
        if not text.strip():
            return PolicyResult(
                passed=False,
                reason="Empty response.",
            )

        return PolicyResult(passed=True)
