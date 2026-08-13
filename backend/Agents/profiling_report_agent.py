from service.profiling_service import generate_profile_report
from schema.state import MLState


def profiling_node(state: MLState) -> dict:

    result = generate_profile_report(
        state["file_path"]
    )

    return {
        "profiling_report": {
            "ReportName": result["report_name"],
            "ReportPath": result["report_path"]
        }
    } 