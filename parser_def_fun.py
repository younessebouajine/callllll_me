from pathlib import Path
from typing import Dict, List, Literal
import json
from models import FunctionDefinition
from pydantic import ValidationError


def load_functions(path: str | Path) -> List[FunctionDefinition]:
    path = Path(path)
    try:
        with path.open("r") as file:
            data = json.load(file)
            # print(data)
            if not isinstance(data, list):
                raise ValueError("The JSON root must be a list.")
            

        return [FunctionDefinition.model_validate(item) for item in data]

    except FileNotFoundError:
        raise FileNotFoundError(f"Function definition file not found: {path}")

    except json.JSONDecodeError as er:
        raise ValueError(f"Invalid JSON: {er}") from er

    except ValidationError as er:
        raise ValueError(f"Invalid function definition:\n{er}") from er
