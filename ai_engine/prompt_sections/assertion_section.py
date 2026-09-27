class AssertionSection:

    @staticmethod
    def build(assertions):

        return f"""
========================================================

Relevant Assertions

{assertions}
"""