from pathlib import Path
import json


class Vocabulary:
    def __init__(self, vocab_path: str | Path) -> None:
        self.vocab_path = Path(vocab_path)

        with self.vocab_path.open("r") as file:
            self.token_to_id: dict[str, int] = json.load(file)

        self.id_to_token: dict[int, str] = {
            token_id: token
            for token, token_id in self.token_to_id.items()
        }

    def get_id(self, token: str) -> int:
        return self.token_to_id[token]

    def get_token(self, token_id: int) -> str:
        return self.id_to_token[token_id]

    def has_token(self, token: str) -> bool:
        return token in self.token_to_id

    def __len__(self) -> int:
        return len(self.token_to_id)