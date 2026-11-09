# Models For Classes

from dataclasses import dataclass, field


@dataclass
class Action:
    type: str  # Whether app, url (browser) or folder   
    target: str  # File path to the target ( URL for browsers )
    delay: float = 0 # Delay in seconds after executing an action ( We will set different values for apps and folders )


@dataclass
class Preset:
    id: str
    name: str  # User defined preset name
    hotkey: str  # User defined shorcut key for the preset
    actions: list[Action] = field(default_factory=list)  # List of actions to be executed in this preset


