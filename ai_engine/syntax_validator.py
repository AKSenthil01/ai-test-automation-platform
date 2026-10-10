import ast


class SyntaxValidator:

    @staticmethod
    def validate(code: str):
        """
        Returns:
            (True, None)  -> if syntax is valid
            (False, error)-> if syntax is invalid
        """
        try:
            ast.parse(code)
            return True, None

        except SyntaxError as e:
            return False, str(e)