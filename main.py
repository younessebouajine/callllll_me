import json
from pathlib import Path

from parser_promet import load_prompts
from parser_def_fun import load_functions
from llm_client import LLMClient
from json_constraint import JsonConstraint
from constrained_decoder import ConstrainedDecoder
from functionselector import FunctionSelector

def main():
    prompts = load_prompts(
        Path("data/input/function_calling_tests.json")
    )

    functions = load_functions(
        Path("data/input/functions_definition.json")
    )

    llm = LLMClient()

    constraint = JsonConstraint(functions)

    selector = FunctionSelector(
        llm,
        functions,
    )

    decoder = ConstrainedDecoder(
        llm,
        constraint,
    )

    results = []
    for prompt in prompts:
        function = selector.select(prompt.prompt)

        parameters = decoder.extract_parameters(
            prompt.prompt,
            function.name,
        )

        results.append(
            {
                "prompt": prompt.prompt,
                "name": function.name,
                "parameters": parameters,
            }
        )
    output_path = Path(
        "data/output/function_calling_results.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False,
    )

if __name__ == "__main__":
    main()