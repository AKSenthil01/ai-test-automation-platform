from typing import List

from sentence_transformers.util import cos_sim

from ai_engine.api_catalog import APICatalog
from ai_engine.base_embedding import BaseEmbedding
from ai_engine.config import TOP_K_APIS


class APISelector:
    """
    Selects the most relevant controller APIs for a given requirement
    using semantic similarity.
    """

    MANDATORY_APIS = [

        "configure_controller",

        "reset_controller"

    ]

    def __init__(self):

        self.model = BaseEmbedding.get_model()

        self.apis = APICatalog.load()

        self.api_embeddings = self.model.encode(

            self.apis,

            convert_to_tensor=True,

            normalize_embeddings=True

        )

    def select(

        self,

        requirement: str,

        top_k: int = TOP_K_APIS,

        debug: bool = False

    ) -> List[str]:

        if not requirement.strip():

            return [

                api

                for api in self.MANDATORY_APIS

                if api in self.apis

            ]

        query_embedding = self.model.encode(

            requirement,

            convert_to_tensor=True,

            normalize_embeddings=True

        )

        scores = cos_sim(

            query_embedding,

            self.api_embeddings

        )[0].cpu().numpy()

        ranked = sorted(

            zip(self.apis, scores),

            key=lambda x: x[1],

            reverse=True

        )

        if debug:

            print()

            print("Top API Matches")

            print("-" * 50)

            for api, score in ranked[:10]:

                print(f"{api:<35} {score:.3f}")

        selected = [

            api

            for api, _ in ranked[:top_k]

        ]

        for api in self.MANDATORY_APIS:

            if api in self.apis and api not in selected:

                selected.append(api)

        return list(dict.fromkeys(selected))