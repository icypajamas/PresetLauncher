from typing import Callable

def register_hotkey(hotkey: str, callback: Callable) -> None:
    raise NotImplementedError("To be Implemented")


# Unregister hotkey reserved at OS level so after program exits, the system can use it
def unregister_all() -> None:
    raise NotImplementedError("To be Implemented")