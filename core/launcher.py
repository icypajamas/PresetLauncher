from core.models import Preset, Action


# Execute a whole preset, each action in order
def execute_preset(preset: Preset):
    raise NotImplementedError("To be Implemented")


# Execute a single action from a preset
def execute_action(action: Action):
    raise NotImplementedError("To be Implemented")