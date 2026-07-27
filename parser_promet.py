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

        if not isinstance(data, list):
            raise ValueError(
                "The JSON root must be a list."
            )

        if not data:
            raise ValueError(
                "JSON file must contain at least one prompt."
            )

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Item {index} must be a JSON object."
                )

            if set(item.keys()) != {"prompt"}:
                raise ValueError(
                    f"Item {index} must contain only the 'prompt' key."
                )

            if not isinstance(item["prompt"], str):
                raise ValueError(
                    f"Prompt {index} must be a string."
                )

            if item["prompt"].strip() == "":
                raise ValueError(
                    f"Prompt {index} cannot be empty."
                )

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