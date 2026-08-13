from schema.state import MLState
from service.upload_service import save_uploaded_file


async def upload_node(state: MLState) -> dict:

    file = state["file"]

    result = await save_uploaded_file(file)

    return {
        "file_path": result["file_path"]
    }