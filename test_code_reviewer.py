from ai_engine.code_reviewer import CodeReviewer
from ai_engine.review_parser import ReviewParser

print("Creating reviewer...")

reviewer = CodeReviewer()

print("Calling review()...")

review = reviewer.review(
    "Verify compressor startup.",
    """
def test_demo():
    configure_controller()
    fake_function()
"""
)

print("Raw review:")
print(repr(review))

print("Parsed review:")
print(ReviewParser.parse(review))