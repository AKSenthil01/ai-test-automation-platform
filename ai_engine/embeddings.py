import os
from typing import List, Union

import numpy as np
import pandas as pd

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """
    Central embedding service.

    Responsibilities
    ----------------
    1. Build FAISS knowledge base
    2. Generate sentence embeddings
    3. Compute cosine similarity
    4. Load embedding models only once (Singleton)
    """

    _instance = None
    _model = None
    _embedding = None

    KNOWLEDGE_FILES = [

        "Controller_API.md",

        "AutomationGuidelines.md",

        "PytestBestPractices.md",

        "AutomationBestPractices.md",

        "PytestExamples.md"

    ]

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            print("\nLoading SentenceTransformer model...")

            cls._model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

        return cls._instance

    def __init__(self):

        if EmbeddingManager._embedding is None:

            EmbeddingManager._embedding = HuggingFaceEmbeddings(

                model_name="sentence-transformers/all-MiniLM-L6-v2"

            )

        self.embedding = EmbeddingManager._embedding

    # ------------------------------------------------------------------
    # Sentence Embeddings
    # ------------------------------------------------------------------

    def encode(
        self,
        texts: Union[str, List[str]]
    ) -> np.ndarray:

        if isinstance(texts, str):
            texts = [texts]

        return self._model.encode(

            texts,

            normalize_embeddings=True

        )

    # ------------------------------------------------------------------
    # Cosine Similarity
    # ------------------------------------------------------------------

    def cosine_similarity(
        self,
        query_vector: np.ndarray,
        vectors: np.ndarray
    ) -> np.ndarray:

        query_vector = np.atleast_2d(query_vector)

        vectors = np.atleast_2d(vectors)

        # Embeddings are normalized during encoding.
        # Therefore dot-product equals cosine similarity.

        return np.dot(query_vector, vectors.T)

    # ------------------------------------------------------------------
    # Build Complete Knowledge Base
    # ------------------------------------------------------------------

    def build_complete_knowledge_base(self):

        documents = []

        testcases = self.load_testcases()
        failures = self.load_failures()
        requirements = self.load_requirements()
        markdown = self.load_markdown()

        documents.extend(testcases)
        documents.extend(failures)
        documents.extend(requirements)
        documents.extend(markdown)

        db = FAISS.from_documents(

            documents,

            self.embedding

        )

        os.makedirs("vector_db", exist_ok=True)

        db.save_local("vector_db")

        print("\nKnowledge Base Statistics")
        print("-" * 40)
        print(f"Test Cases      : {len(testcases)}")
        print(f"Failures        : {len(failures)}")
        print(f"Requirements    : {len(requirements)}")
        print(f"Markdown Docs   : {len(markdown)}")
        print(f"Total Documents : {len(documents)}")
        print("-" * 40)
        print("FAISS index saved to vector_db")

    # ------------------------------------------------------------------
    # Rebuild Vector DB
    # ------------------------------------------------------------------

    def rebuild_vector_db(self):

        print("\nRebuilding FAISS Knowledge Base...\n")

        self.build_complete_knowledge_base()

        print("\nKnowledge Base Rebuilt Successfully.")

    # ------------------------------------------------------------------
    # HVAC Test Cases
    # ------------------------------------------------------------------

    def load_testcases(self):

        docs = []

        path = "knowledge/HVAC_TestCases.xlsx"

        if not os.path.exists(path):
            return docs

        df = pd.read_excel(

            path,

            sheet_name="Test Cases"

        )

        for _, row in df.iterrows():

            docs.append(

                Document(

                    page_content=f"""
Requirement:
{row['Requirement']}

Steps:
{row['Steps']}

Expected Result:
{row['Expected Results']}
""",

                    metadata={

                        "source": "HVAC",

                        "module": row["Requirement"],

                        "testcase": row["Test Case ID"]

                    }

                )

            )

        return docs

    # ------------------------------------------------------------------
    # Historical Failures
    # ------------------------------------------------------------------

    def load_failures(self):

        docs = []

        path = "knowledge/HistoricalFailures.xlsx"

        if not os.path.exists(path):
            return docs

        df = pd.read_excel(path)

        for _, row in df.iterrows():

            docs.append(

                Document(

                    page_content=f"""
Failure:
{row['Failure']}

Root Cause:
{row['Root Cause']}

Fix:
{row['Fix']}

Severity:
{row['Severity']}
""",

                    metadata={

                        "source": "Failure",

                        "module": row["Module"]

                    }

                )

            )

        return docs

    # ------------------------------------------------------------------
    # Requirements
    # ------------------------------------------------------------------

    def load_requirements(self):

        docs = []

        path = "knowledge/Requirements.xlsx"

        if not os.path.exists(path):
            return docs

        df = pd.read_excel(path)

        for _, row in df.iterrows():

            docs.append(

                Document(

                    page_content=f"""
Requirement:
{row['Requirement']}

Priority:
{row['Priority']}
""",

                    metadata={

                        "source": "Requirement",

                        "module": row["Module"]

                    }

                )

            )

        return docs

    # ------------------------------------------------------------------
    # Markdown Knowledge
    # ------------------------------------------------------------------

    def load_markdown(self):

        docs = []

        for filename in self.KNOWLEDGE_FILES:

            path = os.path.join(

                "knowledge",

                filename

            )

            if not os.path.exists(path):
                continue

            with open(path, encoding="utf-8") as f:

                text = f.read()

            docs.append(

                Document(

                    page_content=text,

                    metadata={

                        "source": filename,

                        "module": filename.replace(".md", "")

                    }

                )

            )

        return docs