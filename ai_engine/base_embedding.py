from sentence_transformers import SentenceTransformer

from ai_engine.config import EMBEDDING_MODEL


class BaseEmbedding:
    """
    Singleton embedding model.

    SentenceTransformer loads only once.
    """

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("\nLoading SentenceTransformer model...")

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        return cls._model