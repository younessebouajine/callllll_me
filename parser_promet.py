from pathlib import Path
from typing import List
import json

from pydantic import ValidationError

from models import Prompt


def load_prompts(path: str | Path) -> List[Prompt]:
    path = Path(path)

    try:
        with path.open("r") as file:
            data = json.load(file)

        return [
            Prompt.model_validate(item)
            for item in data
        ]

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Prompt file not found: {path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON:\n{error}"
        ) from error

    except ValidationError as error:
        raise ValueError(
            f"Invalid prompt format:\n{error}"
        ) from error