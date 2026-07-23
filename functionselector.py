from llm_client import LLMClient
from models import FunctionDefinition


class FunctionSelector:
    def __init__(
        self,
        llm: LLMClient,
        functions: list[FunctionDefinition],
    ) -> None:
        self.llm = llm
        self.functions = functions

    def select(
        self,
        prompt: str,
    ) -> FunctionDefinition:
        """
        Select the best function for the user's prompt.
        """

        available_functions = []

        for function in self.functions:
            available_functions.append(
                f"- {function.name}: {function.description}"
            )

        llm_prompt = f"""
Choose the best function.

Available functions:
{chr(10).join(available_functions)}

User request:
{prompt}

Return only the function name.
"""

        input_ids = self.llm.encode(llm_prompt)[0].tolist()

        generated_ids = []

        for _ in range(20):
            logits = self.llm.get_next_token_logits(input_ids)

            next_token = max(
                range(len(logits)),
                key=lambda token_id: logits[token_id],
            )

            input_ids.append(next_token)
            generated_ids.append(next_token)

        generated_text = self.llm.decode(generated_ids).strip()

        for function in self.functions:
            if function.name in generated_text:
                return function

        raise ValueError(
            f"Unknown function returned by model:\n{generated_text}"
        )