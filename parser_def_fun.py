from pathlib import Path
from typing import List
import json
from models import FunctionDefinition
from pydantic import ValidationError


def load_functions(path: str | Path) -> List[FunctionDefinition]:
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
                "JSON file must contain at least one function."
            )

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Item {index} must be a JSON object."
                )

        functions = [
            FunctionDefinition.model_validate(item)
            for item in data
        ]
        dubl = set()
        for function in functions:
            if function.name in dubl:
                raise ValueError(
                    f"Duplicate function name: '{function.name}'."
                )
            dubl.add(function.name)

        return functions

    except FileNotFoundError as er:
        raise FileNotFoundError(
            f"Function definition file not found: {path}"
            ) from er

    except json.JSONDecodeError as er:
        raise ValueError(
            f"Invalid JSON: {er}"
            ) from er

    except ValidationError as er:
        raise ValueError(
            f"Invalid function definition:\n{er}"
            ) from er
