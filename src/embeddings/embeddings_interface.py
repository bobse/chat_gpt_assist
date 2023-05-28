from abc import ABC, abstractmethod


class EmbeddingsInterface(ABC):
    @abstractmethod
    def get_embeddings(self, sentence: str):
        raise NotImplementedError()

    @abstractmethod
    def insert_into_db(self, model_response: dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_similar(self, user_input: str, limit: int = 10) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def empty(self) -> None:
        raise NotImplementedError()
