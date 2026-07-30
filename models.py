from pydantic import BaseModel, ConfigDict, field_validator
from typing import Dict, Literal
import keyword


class Prompt(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError(
                "Prompt cannot be empty."
            )
        return value



class Parameter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    type: Literal["number", "string", "boolean", "integer"]

class FunctionDefinition(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    name: str
    description: str
    parameters: Dict[str, Parameter]
    returns: Parameter

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.isidentifier():
            raise ValueError(
                "Invalid Python identifier"
            )
        if keyword.iskeyword(value):
            raise ValueError(
                "Function name cannot be a Python keyword."
            )
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError(
                "Description cannot be empty."
            )
        return value
    @field_validator("parameters")
    @classmethod
    def validate_parameter_names(
        cls,
        value: Dict[str, Parameter],
    ) -> Dict[str, Parameter]:
        for parmeter_name in value:
            if not parmeter_name.isidentifier():
                raise ValueError(
                    f"Invalid parameter name: '{parmeter_name}'."
                )
            if keyword.iskeyword(parmeter_name):
                raise ValueError(
                    f"'{parmeter_name}' is a Python keyword."
                )
        return value
