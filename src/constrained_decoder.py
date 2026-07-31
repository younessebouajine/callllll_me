import json
from src.llm_client import LLMClient
from src.json_constraint import JsonConstraint


class ConstrainedDecoder:
    def __init__(
        self,
        llm: LLMClient,
        constraint: JsonConstraint,
    ) -> None:
        self.llm = llm
        self.constraint = constraint

    def extract_parameters(
        self,
        prompt: str,
        function_name: str,
    ) -> dict:

        parameter_names = self.constraint.get_parameter_names(
            function_name,
        )

        schema = {}

        for parameter_name in parameter_names:
            schema[parameter_name] = (
                self.constraint.get_parameter_type(
                    function_name,
                    parameter_name,
                )
            )

        llm_prompt = self.build_prompt(
            prompt,
            function_name,
            schema,
        )

        input_ids = self.llm.encode(
            llm_prompt,
        )[0].tolist()

        generated_ids = []

        generated_text = ""
        json_text = None

        for _ in range(150):
            logits = self.llm.get_next_token_logits(
                input_ids,
            )
            # print(list(range(len(logits))))
            

            next_token = self.valid_token(
                logits,
                list(range(len(logits))),
            )

            input_ids.append(next_token)
            generated_ids.append(next_token)

            generated_text = self.llm.decode(
                generated_ids,
            )

            try:
                json_text = self.extract_json(
                    generated_text,
                )
                break
            except ValueError:
                continue

        if json_text is None:
            raise ValueError(
                f"No complete JSON generated:\n{generated_text}"
            )

        try:
            parameters = json.loads(
                json_text,
            )
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON:\n{json_text}"
            )

        for parameter_name in parameter_names:
            if parameter_name not in parameters:
                raise ValueError(
                    f"Missing parameter '{parameter_name}'"
                )

        for parameter_name in parameter_names:
            if (
                self.constraint.get_parameter_type(
                    function_name,
                    parameter_name
                ) == "number"
            ):
                parameters[parameter_name] = float(
                    parameters[parameter_name]
                )


        return {
            parameter: parameters[parameter]
            for parameter in parameter_names
        }

    def build_prompt(
        self,
        prompt: str,
        function_name: str,
        schema: dict,
    ) -> str:

        example = self.get_example(
            function_name,
        )

        return f"""
You are a JSON generator.

Generate ONLY the parameters of the selected function.

Rules:
- Return ONLY one JSON object.
- Do not explain.
- Do not use markdown.
- Do not write anything before or after the JSON.
- Use exactly the parameter names from the schema.

Function:
{function_name}

Parameter Schema:
{schema}

Example:

{example}

User Request:
{prompt}

JSON:
"""

    def get_example(
        self,
        function_name: str,
    ) -> str:

        examples = {
            "fn_add_numbers":
"""
User:
What is the sum of 2 and 3?

Output:
{"a": 2, "b": 3}
""",

            "fn_greet":
"""
User:
Greet John

Output:
{"name": "John"}
""",

            "fn_reverse_string":
"""
User:
Reverse the string "hello"

Output:
{"s": "hello"}
""",

            "fn_get_square_root":
"""
User:
What is the square root of 16?

Output:
{"a": 16}
""",

            "fn_substitute_string_with_regex":
"""
User:
Replace all vowels in "Programming is fun" with asterisks

Output:
{
    "source_string": "Programming is fun",
    "regex": "[aeiouAEIOU]",
    "replacement": "*"
}
"""
        }

        return examples.get(
            function_name,
            "",
        )

    def extract_json(
        self,
        text: str,
    ) -> str:

        start = text.find("{")

        if start == -1:
            raise ValueError(
                "No JSON object found."
            )

        depth = 0

        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1

            elif text[i] == "}":
                depth -= 1

                if depth == 0:
                    return text[start:i + 1]

        raise ValueError(
            "Incomplete JSON object."
        )

    def valid_token(
        self,
        logits: list[float],
        valid_token_ids: list[int],
    ) -> int:

        if not valid_token_ids:
            raise ValueError(
                "No valid tokens available."
            )

        return max(
            valid_token_ids,
            key=lambda token_id: logits[token_id],
        )