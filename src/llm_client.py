from llm_sdk import Small_LLM_Model


class LLMClient:
    def __init__(self) -> None:
        self.model = Small_LLM_Model()

    def encode(self, text: str):
        return self.model.encode(text)

    def decode(self, ids):
        return self.model.decode(ids)

    def get_next_token_logits(self, input_ids):
        return self.model.get_logits_from_input_ids(input_ids=input_ids)

    def get_vocab_file_path(self) -> str:
        return self.model.get_path_to_vocab_file()