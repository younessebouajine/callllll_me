from pathlib import Path
from typing import List
import json
from pydantic import ValidationError
from models import Prompt


def load_prompts(path: str | Path) -> List[Prompt]:
    try:
        with Path(path).open("r") as file:
            data = json.load(file)
            # print(data)
            if not data:
                raise ValueError("JSON file must contain at least one prompt.")
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Each item must be a JSON object.")
                if set(item.keys()) != {"prompt"}:
                    raise ValueError("Each item must contain only the 'prompt' key.")
                if item["prompt"].strip() == "":
                    raise ValueError("The value of 'prompt' cannot be empty.")

        
        # prompts = []
        
        # for item in data:
        #     validated_prompt = Prompt.model_validate(item)
        #     prompts.append(validated_prompt)
        # return prompts
        return [Prompt.model_validate(item) for item in data]

    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {path}")

    except json.JSONDecodeError as er:
        raise ValueError(f"Invalid JSON: {er}") from er
    except ValidationError as er:
        raise ValueError(f"Invalid prompt format:\n{er}") from er
