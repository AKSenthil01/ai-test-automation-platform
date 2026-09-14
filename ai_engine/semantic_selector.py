from ai_engine.embeddings import EmbeddingManager


class SemanticSelector:
    """
    Base class for all semantic retrieval components.

    Child classes only need to supply a list of items.

    This class performs:
        • embedding generation
        • cosine similarity
        • ranking
        • top-k retrieval
    """

    def __init__(self, items):

        self.items = items

        self.embedding = EmbeddingManager()

        self.item_vectors = self.embedding.encode(items)

    def select(self, query, top_k=5):

        query_vector = self.embedding.encode(query)

        scores = self.embedding.cosine_similarity(
            query_vector,
            self.item_vectors
        )[0]

        ranked = sorted(
            zip(self.items, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item
            for item, _
            in ranked[:top_k]
        ]