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

    # Initial state --> graph ko btaana padega ki initial state kya hai 
    state = {
        "file_path": file_path,
        "profile_state": {},
        "summary_state": {},
        "column_identifier_state": {},
        "cleaning_plan": {},
        "cleaning_state": {}
    }

    # Run ML pipeline
    final_state = await ml_graph.ainvoke(state)

    return {
        "message":"File Loaded successfully",
        "file_path": final_state.get("file_path"),
        "cleaned_file_path": final_state.get("cleaned_file_path"),
        "profile":final_state.get("profile_state"),
        "summary":final_state.get("summary_state"),
        "column_identifier": final_state.get("column_identifier_state"),
        "cleaning_plan": final_state.get("cleaning_plan"),
        "clean_state" : final_state.get("cleaning_state")

    }