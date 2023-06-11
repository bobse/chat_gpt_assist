import json
from pathlib import Path
import lancedb

from config import config
from embeddings.embeddings_interface import EmbeddingsInterface


class EmbeddingsLocal(EmbeddingsInterface):
    def __init__(self, table_name: str) -> None:
        self.db = lancedb.connect(str(config.EMBEDDINGS_DB))
        try:
            self.table = self.db.create_table(
                table_name,
                data=[
                    {
                        "vector": self.get_embeddings("initial_setup"),
                        "data": "{}",
                    }
                ],
            )
        except:
            self.table = self.db.open_table(table_name)

    def get_embeddings(self, sentence: str):
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "paraphrase-albert-small-v2",
            cache_folder=Path(config.BASE_PATH, "temp/sentence_transformers"),
        )
        # model = SentenceTransformer(
        #     "all-MiniLM-L6-v2",
        #     cache_folder=Path(config.BASE_PATH, "temp/sentence_transformers"),
        # )
        return model.encode([sentence])[0]

    def insert_into_db(self, model_response: dict) -> None:
        self.table.add(
            [
                {
                    "vector": self.get_embeddings(model_response["user_input"]),
                    "data": json.dumps(model_response),
                }
            ]
        )

    def get_similar(self, user_input: str, limit: int = 10):
        results = (
            self.table.search(self.get_embeddings(user_input))
            .select(["data"])
            .limit(limit)
            .to_df()
            .to_dict("records")
        )

        return [{"data": json.loads(r["data"]), "score": r["score"]} for r in results]

    def empty(self):
        return len(self.table) == 1
