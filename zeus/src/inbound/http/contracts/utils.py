import json
from pathlib import Path


def load_example(*, name: str) -> dict[str, object]:
    example_file = Path(__file__).parent / "examples" / name

    with open(example_file, "r") as file:
        return json.load(file)
