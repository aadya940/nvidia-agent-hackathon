from .agents import core_loop

# Export root_agent for ADK (ADK looks for this specific name)
root_agent = core_loop

__all__ = ["root_agent"]
