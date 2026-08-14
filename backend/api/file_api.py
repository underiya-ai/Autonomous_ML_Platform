from fastapi import APIRouter, UploadFile, File

from service.upload_service import save_uploaded_file
from controller.graph import build_ml_graph


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


ml_graph = build_ml_graph()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Save uploaded file
    result = await save_uploaded_file(file)

    # Get saved file path
    file_path = result["file_path"]

    # Initial state
    state = {
        "file_path": file_path,
        "profile_state": {},
        "summary_state": {}
    }

    # Run ML pipeline
    final_state = await ml_graph.ainvoke(state)

    return {
        "message": "File uploaded and processed successfully",
        "file": result,
        "profile": final_state.get("profile_state", {}),
        "summary": final_state.get("summary_state", {})
    }