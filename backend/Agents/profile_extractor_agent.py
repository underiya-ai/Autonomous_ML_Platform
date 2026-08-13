from service.profile_extractor import extract_profile_data
from schema.state import MLState


def profile_extractor_node(state: MLState) -> dict:
    """
    Extract structured profiling information from the uploaded dataset.
    """

    file_path = state["file_path"]

    # Extract dataset profile
    profile_state = extract_profile_data(file_path)

    return {
        "profile_state": profile_state
    }