from langchain_community.vectorstores import FAISS
from ai_engine.embeddings import EmbeddingManager


class RAGRetriever:

    def __init__(self):

        embedding = EmbeddingManager().embedding

        self.db = FAISS.load_local(
            "vector_db",
            embedding,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query, top_k=10):
        return self.db.similarity_search(
            query,
            k=top_k
        )