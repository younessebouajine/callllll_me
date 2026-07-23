from llm_client import LLMClient
from json_constraint import JsonConstraint


class FunctionTokenSequences:
    def __init__(
        self,
        llm: LLMClient,
        constraint: JsonConstraint,
    ) -> None:
        self.llm = llm
        self.constraint = constraint

    def get_sequences(self) -> dict[str, list[int]]:
        """
        Return the token sequence for each function name.
        """

        token_sequences: dict[str, list[int]] = {}

        for function_name in self.constraint.get_function_names():
            token_sequences[function_name] = (
                self.llm.encode(function_name)[0].tolist()
            )

        return token_sequences