# from ai_engine.quality_report import QualityReport
#
# report = QualityReport()
#
# report.set_requirement(
#     "Verify A2L leak alarm during compressor startup."
# )
#
# report.set_generation_time(5.82)
#
# report.set_knowledge_docs(3)
#
# report.set_selected_apis([
#     "configure_controller",
#     "start_compressor",
#     "verify_a2l_alarm",
#     "clear_alarm"
# ])
#
# report.set_syntax(True)
#
# report.set_allowed_api_check(True)
#
# report.set_hallucination_check(True)
#
# report.set_review(True)
#
# report.set_iterations(1)
#
# report.print_report()
#
# report.save_json()
from ai_engine.quality_report import QualityReport

report = QualityReport()

result = report.generate(

    requirement="Verify compressor startup",

    code="""
import pytest

def test_start():

    configure_controller()

    start_compressor()

    assert get_compressor_status()=="RUNNING"

    stop_compressor()

    reset_controller()
""",

    review_iterations=2,

    syntax_ok=True,

    api_ok=True

)

print(result)