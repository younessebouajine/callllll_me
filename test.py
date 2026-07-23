# from pydantic import BaseModel, ValidationError


# class Name:
#     def __init__(self, name: str, age : int) -> None:
#         self.name = name
#         self.age = age
#     def __repr__(self):
#         return f"name: {self.name}, age: {self.age}"


# class User(BaseModel):
#     first_name: str
#     age: int


# name = Name("ali", "hello")
# user = User(first_name="Ahmed", age= "55")
# print(name, "\n", str(user))

# from pathlib import Path
# import json
# from pydantic import BaseModel


# class Prompt(BaseModel):
#     prompt: str

# def load_file(path: str | Path):
#     try:
#         with open(path, "r") as file:
#             data = json.load(file)
        
#         return [Prompt.model_validate(item) for item in data]
#     except FileNotFoundError as e:
#         raise ()

# from llm_sdk import Small_LLM_Model
import sys
from json_constraint import JsonConstraint
from llm_client import LLMClient
from constrained_decoder import ConstrainedDecoder
# from vocabulary import Vocabulary
from functionselector import FunctionSelector
# vocabulary = Vocabulary()



from parser_def_fun import load_functions
from functiontokensequences import FunctionTokenSequences
llm = LLMClient()



token_sequences = FunctionTokenSequences(
    llm,
    load_functions("data/input/functions_definition.json"),
)

print(token_sequences.get_sequences())


# constraint = JsonConstraint
# functionelector = FunctionSelector(llm, load_functions("data/input/functions_definition.json"))
# text = "What is the sum of 2 and 3?"

# functionelector.select(text)
# sys.exit()




# llm_test = Small_LLM_Model()

# ls = ConstrainedDecoder(llm, JsonConstraint)
# ls.generate(text)