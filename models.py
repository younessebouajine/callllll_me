from pydantic import BaseModel
from typing import Dict, Literal


class Prompt(BaseModel):
    prompt: str


class Parameter(BaseModel):
    type: Literal["number", "string", "boolean", "integer"]

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Parameter]
    returns: Parameter