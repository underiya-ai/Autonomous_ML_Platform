from schema.state import MLState

from service.cleaning_service import clean_dataset


def cleaning_executor(state: MLState) -> dict:

    result = clean_dataset(file_path=state["file_path"],cleaning_plan=state["cleaning_plan"])

    return {
        "cleaning_state": result,

        "cleaned_file_path": result[
            "cleaned_file_path"
        ]
    }