
from models import Prompt, FunctionDefinition


def build_prompt(
    prompt: Prompt,
    functions: list[FunctionDefinition]
) -> str:
    """
    Build the prompt that will be sent to the LLM.

    Args:
        prompt: The user's request.
        functions: Available function definitions.

    Returns:
        A formatted string describing the available functions
        and the user's request.
    """

    sections: list[str] = []

    sections.append(
        "You are a function calling assistant.\n"
        "Your task is to:\n"
        "1. Choose the best function for the user's request.\n"
        "2. Extract the correct arguments.\n"
        "3. Return only valid JSON.\n"
    )

    sections.append("Available functions:\n")

    for function in functions:
        sections.append(f"Function: {function.name}")
        sections.append(f"Description: {function.description}")

        sections.append("Parameters:")

        for param_name, param in function.parameters.items():
            sections.append(
                f"- {param_name}: {param.type}"
            )

        sections.append(
            f"Returns: {function.returns.type}"
        )

        sections.append("-" * 40)

    sections.append("\nUser request:")
    sections.append(prompt.prompt)

    sections.append(
        "\nReturn only valid JSON and nothing else."
    )

    return "\n".join(sections)