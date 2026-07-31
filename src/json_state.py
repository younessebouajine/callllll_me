class JsonState:
    def __init__(self) -> None:
        self.current_tokens: list[int] = []
        self.target_tokens: list[int] = []

    def reset(self) -> None:
        self.current_tokens.clear()
        self.target_tokens.clear()

    def start_new_sequence(
        self,
        token_sequence: list[int],
    ) -> None:
        self.current_tokens = []
        self.target_tokens = token_sequence.copy()

    def add_token(
        self,
        token_id: int,
    ) -> None:
        self.current_tokens.append(token_id)

    def get_valid_tokens(self) -> list[int]:
        """
        Return the next valid token.
        """
        if len(self.current_tokens) >= len(self.target_tokens):
            return []

        return [
            self.target_tokens[len(self.current_tokens)]
        ]

    def finished(self) -> bool:
        return len(self.current_tokens) == len(self.target_tokens)