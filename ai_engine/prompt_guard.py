import re


class PromptGuard:
    """
    Prompt sanitation and validation utilities.

    Responsibilities
    ----------------
    - Normalize whitespace
    - Remove control characters
    - Remove common prompt-injection phrases
    - Enforce maximum prompt size
    - Estimate token count
    """

    MAX_CHARS = 16000

    BLOCKED_PATTERNS = [

        r"ignore\s+previous\s+instructions",

        r"forget\s+all\s+instructions",

        r"system\s+prompt",

        r"developer\s+message",

        r"you\s+are\s+chatgpt",

        r"act\s+as",

        r"jailbreak",

    ]

    # ---------------------------------------------------------
    # Main Entry
    # ---------------------------------------------------------

    @classmethod
    def clean(

            cls,

            prompt: str,

            max_chars: int = None,

            debug: bool = False

    ) -> str:

        if not prompt:

            return ""

        if max_chars is None:

            max_chars = cls.MAX_CHARS

        # ---------------------------------------------
        # Normalize line endings
        # ---------------------------------------------

        prompt = prompt.replace("\r\n", "\n")

        prompt = prompt.replace("\r", "\n")

        # ---------------------------------------------
        # Remove control characters
        # ---------------------------------------------

        prompt = "".join(

            ch

            for ch in prompt

            if ch == "\n" or ch == "\t" or ord(ch) >= 32

        )

        # ---------------------------------------------
        # Collapse excessive blank lines
        # ---------------------------------------------

        prompt = re.sub(

            r"\n{3,}",

            "\n\n",

            prompt

        )

        # ---------------------------------------------
        # Collapse spaces
        # ---------------------------------------------

        prompt = re.sub(

            r"[ \t]{2,}",

            " ",

            prompt

        )

        # ---------------------------------------------
        # Remove prompt injection phrases
        # ---------------------------------------------

        for pattern in cls.BLOCKED_PATTERNS:

            prompt = re.sub(

                pattern,

                "",

                prompt,

                flags=re.IGNORECASE

            )

        prompt = prompt.strip()

        # ---------------------------------------------
        # Truncate if too large
        # ---------------------------------------------

        if len(prompt) > max_chars:

            prompt = prompt[:max_chars]

        if debug:

            print("=" * 80)
            print("PROMPT GUARD")
            print("=" * 80)
            print(f"Characters : {len(prompt)}")
            print(f"Words      : {len(prompt.split())}")
            print(f"Est Tokens : {cls.estimate_tokens(prompt)}")

        return prompt

    # ---------------------------------------------------------
    # Token Estimation
    # ---------------------------------------------------------

    @staticmethod
    def estimate_tokens(prompt: str) -> int:

        if not prompt:

            return 0

        return max(

            1,

            len(prompt) // 4

        )

    # ---------------------------------------------------------
    # Validate Prompt
    # ---------------------------------------------------------

    @classmethod
    def validate(cls, prompt: str):

        if not prompt.strip():

            raise ValueError("Prompt is empty.")

        if len(prompt) > cls.MAX_CHARS:

            raise ValueError(

                f"Prompt exceeds {cls.MAX_CHARS} characters."

            )

    # ---------------------------------------------------------
    # Backward Compatibility
    # ---------------------------------------------------------

    @classmethod
    def protect(cls, prompt: str) -> str:

        return cls.clean(prompt)