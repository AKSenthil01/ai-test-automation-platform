class APISection:

    @staticmethod
    def build(apis):

        api_text = "\n".join(
            f"- {api}"
            for api in apis
        )

        return f"""
========================================================

Allowed Controller APIs

{api_text}
"""