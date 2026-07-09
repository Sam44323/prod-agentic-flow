from collections.abc import Callable
from typing import Any


# this is a wrapper for the tools to catch any exceptions and raise a RuntimeError
def execute_tool(
    tool: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    try:
        return tool(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Tool execution failed: {e}") from e
