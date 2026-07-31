from src.models import FunctionDefinition


class JsonConstraint:
    def __init__(self, functions: list[FunctionDefinition]) -> None:
        self.functions = functions

    def get_function_names(self) -> list[str]:
        return [function.name for function in self.functions]

    def get_function(self, name: str) -> FunctionDefinition | None:
        for function in self.functions:
            if function.name == name:
                return function
        return None

    def get_parameter_names(self, function_name: str) -> list[str]:
        function = self.get_function(function_name)

        if function is None:
            return []

        return list(function.parameters.keys())

    def get_parameter_type(
        self,
        function_name: str,
        parameter_name: str,
    ) -> str | None:
        function = self.get_function(function_name)

        if function is None:
            return None

        parameter = function.parameters.get(parameter_name)

        if parameter is None:
            return None

        return parameter.type