from models import Preset

# Load all saved presets to memory
def load_presets(path: str) -> list[Preset]:
    raise NotImplementedError("To be Implemented")

# Save all presets to disk (overwrite cuz it's safer)
def save_presets(preset: list[Preset], folder: str = "presets") -> None:
    raise NotImplementedError("To be Implemented")