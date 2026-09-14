from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class RAGRetriever:

    def __init__(self):

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

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