from llm_client import LLMClient
from vocabulary import Vocabulary

llm = LLMClient()
vocabulary = Vocabulary(llm.get_vocab_file_path())

print(f"vocab size: {len(vocabulary)}")

def test_llm_client():
    # print(vocab.get_id("{"))
    # print(vocab.get_id("}"))
    # print(vocab.get_id(":"))
    # print(vocab.get_id(","))
    # print("=" * 40)
    # print(vocab.get_token(90))
    # print(vocab.get_token(92))
    # print(vocab.get_token(25))
    # print(vocab.get_token(11))
    print(vocabulary.has_token("fn_add_numbers"))
    print(vocabulary.has_token("fn_greet"))
    print(vocabulary.has_token("fn_reverse_string"))


test_llm_client()