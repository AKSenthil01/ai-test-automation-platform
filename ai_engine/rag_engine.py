import os
from typing import List, Dict, Optional, Union

from langchain_community.vectorstores import FAISS

from ai_engine.embeddings import EmbeddingManager


class RAGEngine:
    """
    Central Retrieval-Augmented Generation engine.

    Responsibilities
    ----------------
    • Load FAISS only once
    • Retrieve semantic knowledge
    • Filter by source
    • Return metadata if requested
    """

    _db = None

    VECTOR_DB = "vector_db"

    def __init__(self):

        if RAGEngine._db is None:

            if not os.path.exists(self.VECTOR_DB):

                raise FileNotFoundError(

                    "vector_db not found. "

                    "Run EmbeddingManager.build_complete_knowledge_base() first."

                )

            print("\nLoading Knowledge Base...")

            embedding = EmbeddingManager().embedding

            RAGEngine._db = FAISS.load_local(

                self.VECTOR_DB,

                embedding,

                allow_dangerous_deserialization=True

            )

        self.db = RAGEngine._db

    # --------------------------------------------------------
    # Generic Retrieval
    # --------------------------------------------------------

    def retrieve(

            self,

            requirement: str,

            top_k: int = 3,

            source: Optional[str] = None,

            return_metadata: bool = False,

            debug: bool = False

    ) -> Union[str, List[Dict]]:

        docs = self.db.similarity_search_with_score(

            requirement,

            k=top_k

        )

        results = []

        for doc, score in docs:

            if source:

                if doc.metadata.get("source") != source:

                    continue

            if return_metadata:

                results.append({

                    "content": doc.page_content,

                    "metadata": doc.metadata,

                    "score": float(score)

                })

            else:

                results.append(doc.page_content)

        if debug:

            print()

            print("Retrieved Knowledge")

            print("-" * 60)

            if return_metadata:

                for item in results:

                    print(

                        f"{item['metadata'].get('source')}"

                        f"  Score={item['score']:.3f}"

                    )

            else:

                print(f"{len(results)} document(s) retrieved.")

        if return_metadata:

            return results

        return "\n\n".join(results)

    # --------------------------------------------------------
    # Convenience Wrappers
    # --------------------------------------------------------

    def retrieve_testcases(

            self,

            requirement: str,

            top_k: int = 3

    ):

        return self.retrieve(

            requirement,

            top_k=top_k,

            source="HVAC"

        )

    def retrieve_failures(

            self,

            requirement: str,

            top_k: int = 5

    ):

        return self.retrieve(

            requirement,

            top_k=top_k,

            source="Failure"

        )

    def retrieve_requirements(

            self,

            requirement: str,

            top_k: int = 5

    ):

        return self.retrieve(

            requirement,

            top_k=top_k,

            source="Requirement"

        )

    def retrieve_api_docs(

            self,

            requirement: str,

            top_k: int = 3

    ):

        return self.retrieve(

            requirement,

            top_k=top_k,

            source="Controller_API.md"

        )