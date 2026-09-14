from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class SmartRetriever:

    def __init__(self):

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.db = FAISS.load_local(
            "vector_db",
            embedding,
            allow_dangerous_deserialization=True
        )

    def retrieve(

            self,

            query,

            modules=None,

            sources=None,

            top_k=10

    ):

        # Retrieve more documents than required
        docs = self.db.similarity_search(
            query,
            k=top_k * 5
        )

        filtered = []

        for doc in docs:

            keep = True

            # ----------------------------
            # Filter by HVAC module
            # ----------------------------

            if modules:

                module = doc.metadata.get(
                    "module",
                    ""
                ).lower()

                keep = any(
                    m.lower() in module
                    for m in modules
                )

            # ----------------------------
            # Filter by document source
            # ----------------------------

            if keep and sources:

                source = doc.metadata.get(
                    "source",
                    ""
                )

                keep = source in sources

            if keep:
                filtered.append(doc)

        # If too few documents remain,
        # fall back to similarity results.

        if len(filtered) < top_k:

            filtered.extend(docs)

        # Remove duplicates

        unique = []

        seen = set()

        for doc in filtered:

            text = doc.page_content

            if text not in seen:

                seen.add(text)

                unique.append(doc)

        return unique[:top_k]