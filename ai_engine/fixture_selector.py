import os
from typing import List

from sentence_transformers.util import cos_sim

from ai_engine.base_embedding import BaseEmbedding


class FixtureSelector:
    """
    Selects the most relevant pytest fixtures
    using semantic similarity.
    """

    _blocks = None
    _embeddings = None

    DEFAULT_FILE = "knowledge/PytestFixtures.md"

    def __init__(self):

        self.model = BaseEmbedding.get_model()

        if FixtureSelector._blocks is None:

            FixtureSelector._blocks = self._load_fixtures()

            FixtureSelector._embeddings = self.model.encode(

                FixtureSelector._blocks,

                convert_to_tensor=True,

                normalize_embeddings=True

            )

        self.blocks = FixtureSelector._blocks

        self.embeddings = FixtureSelector._embeddings

    # ----------------------------------------------------------
    # Load Fixtures
    # ----------------------------------------------------------

    def _load_fixtures(self) -> List[str]:

        if not os.path.exists(self.DEFAULT_FILE):

            print(f"WARNING: {self.DEFAULT_FILE} not found.")

            return []

        with open(

                self.DEFAULT_FILE,

                encoding="utf-8"

        ) as f:

            text = f.read()

        blocks = [

            block.strip()

            for block in text.split(

                "------------------------------------------------"

            )

            if block.strip()

        ]

        return blocks

    # ----------------------------------------------------------
    # Select Fixtures
    # ----------------------------------------------------------

    def select(

            self,

            requirement: str,

            top_k: int = 2,

            debug: bool = False

    ) -> List[str]:

        if not self.blocks:

            return []

        query = self.model.encode(

            requirement,

            convert_to_tensor=True,

            normalize_embeddings=True

        )

        scores = cos_sim(

            query,

            self.embeddings

        )[0].cpu().numpy()

        ranked = sorted(

            zip(self.blocks, scores),

            key=lambda x: x[1],

            reverse=True

        )

        if debug:

            print()

            print("Top Matching Fixtures")

            print("-" * 60)

            for _, score in ranked[:top_k]:

                print(f"Similarity : {score:.3f}")

                print("-" * 60)

        return [

            block

            for block, _

            in ranked[:top_k]

        ]