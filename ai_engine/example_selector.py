import os
import re
from typing import List

from sentence_transformers.util import cos_sim

from ai_engine.base_embedding import BaseEmbedding


class ExampleSelector:
    """
    Selects the most relevant pytest examples
    using semantic similarity.
    """

    _examples = None
    _embeddings = None

    DEFAULT_FILE = "knowledge/PytestExamples.md"

    def __init__(self):

        self.model = BaseEmbedding.get_model()

        if ExampleSelector._examples is None:

            ExampleSelector._examples = self._load_examples()

            ExampleSelector._embeddings = self.model.encode(

                ExampleSelector._examples,

                convert_to_tensor=True,

                normalize_embeddings=True

            )

        self.examples = ExampleSelector._examples

        self.embeddings = ExampleSelector._embeddings

    # ----------------------------------------------------------
    # Load Examples
    # ----------------------------------------------------------

    def _load_examples(self) -> List[str]:

        if not os.path.exists(self.DEFAULT_FILE):

            print(f"WARNING: {self.DEFAULT_FILE} not found.")

            return []

        with open(

                self.DEFAULT_FILE,

                encoding="utf-8"

        ) as f:

            text = f.read()

        return self._split_examples(text)

    # ----------------------------------------------------------
    # Split Markdown
    # ----------------------------------------------------------

    def _split_examples(
            self,
            text: str
    ) -> List[str]:

        matches = re.split(

            r"(?=Example\s+\d+)",

            text

        )

        examples = []

        for item in matches:

            item = item.strip()

            if len(item) > 20:

                examples.append(item)

        return examples

    # ----------------------------------------------------------
    # Select Examples
    # ----------------------------------------------------------

    def select(

            self,

            requirement: str,

            top_k: int = 3,

            debug: bool = False

    ) -> List[str]:

        if not self.examples:

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

            zip(self.examples, scores),

            key=lambda x: x[1],

            reverse=True

        )

        if debug:

            print()

            print("Top Matching Examples")

            print("-" * 60)

            for _, score in ranked[:top_k]:

                print(f"Similarity : {score:.3f}")

                print("-" * 60)

        return [

            example

            for example, _

            in ranked[:top_k]

        ]