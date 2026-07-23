# from typing import List
# from models import FunctionDefinition

# class JsonConstraint:
#     def __init__(self, functions:List[FunctionDefinition]) -> None:
#         self.functions = functions

#     def get_valid_tokens(self, generated_text: str, selected_function: FunctionDefinition) -> List[str]:
#         generated_text = generated_text.strip()

#         if generated_text == "":
#             return ["{"]

#         if generated_text == "{":
#             return ['"name"']

#         if generated_text.endswith('"name"'):
#             return [":"]

#         if generated_text.endswith('"name":'):
#             return [f'"{function.name}"' for function in self.functions]

#         if (
#             selected_function is not None
#             and generated_text.endswith(f'"{selected_function.name}"')
#         ):
#             return [","]

#         if generated_text.endswith(","):
#             return ['"parameters"']

#         if generated_text.endswith('"parameters"'):
#             return [":"]

#         if generated_text.endswith('"parameters":'):
#             return ["{"]

#         if (
#             selected_function is not None
#             and generated_text.endswith("{")
#         ):
#             return [
#                 f'"{parameter}"'
#                 for parameter in selected_function.parameters.keys()
#             ]

#         return []


from models import FunctionDefinition


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