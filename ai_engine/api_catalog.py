from ai_engine.api_extractor import APIExtractor


class APICatalog:

    _cache = None

    @classmethod
    def load(cls):
        """
        Returns the complete list of controller APIs.
        Uses caching so Controller_API.md is parsed only once.
        """
        if cls._cache is None:
            cls._cache = APIExtractor.extract()

        return cls._cache

    @classmethod
    def as_prompt(cls):
        """
        Returns all APIs formatted for an LLM prompt.
        """
        text = ""

        for api in cls.load():
            text += f"- {api}()\n"

        return text