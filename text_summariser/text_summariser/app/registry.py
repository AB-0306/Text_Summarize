from typing import Callable, Dict, Any

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._conditions: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        """Register a node function (State -> State)"""
        self._tools[name] = func

    def register_condition(self, name: str, func: Callable):
        """Register a condition function (State -> str)"""
        self._conditions[name] = func

    def get_tool(self, name: str) -> Callable:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def get_condition(self, name: str) -> Callable:
        if name not in self._conditions:
            raise ValueError(f"Condition '{name}' not found in registry.")
        return self._conditions[name]

# Global instance
registry = ToolRegistry()