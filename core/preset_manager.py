
import json
from pathlib import Path
from models import Preset, Action


# Load all saved presets
def load_presets(path):
    folder = Path(path)
    presets = []

    for file in folder.glob("*.json"):
        print("Reading file:", file)

        with open(file, "r") as f:
            data = json.load(f)

        actions = []

        for action_data in data["actions"]:
            action = Action(
                type=action_data["type"],
                target=action_data["target"],
                delay=action_data["delay"]
            )
            actions.append(action)

        preset = Preset(
            id=data["id"],
            name=data["name"],
            hotkey=data["hotkey"],
            actions=actions
        )

        presets.append(preset)

    return presets


# Save all presets to disk
def save_presets(presets: list[Preset], folder: str = "presets") -> None:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for preset in presets:
        actions = []

        for action in preset.actions:
            action_data = {
                "type": action.type,
                "target": action.target,
                "delay": action.delay
            }
            actions.append(action_data)

        preset_data = {
            "id": preset.id,
            "name": preset.name,
            "hotkey": preset.hotkey,
            "actions": actions
        }

        file_path = folder / f"{preset.id}.json"

        with open(file_path, "w") as f:
            json.dump(preset_data, f, indent=4)
