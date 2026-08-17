from fastapi import APIRouter, UploadFile, File
from service.upload_service import save_uploaded_file
from controller.graph import build_ml_graph
from langgraph.types import Command
import uuid


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

    # Unique thread for this pipeline execution
    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    # Initial state
    state = {
        "file_path": file_path,
        "profile_state": {},
        "summary_state": {},
        "column_identifier_state": {},
        "cleaning_plan": {},
        "cleaning_state": {}
    }

    # Run ML pipeline
    final_state = await ml_graph.ainvoke(
        state,
        config=config
    )

    return {
        "message": "Column selection required",
        "thread_id": thread_id,
        "file_path": final_state.get("file_path"),
        "profile": final_state.get("profile_state"),
        "summary": final_state.get("summary_state"),
        "column_identifier": final_state.get("column_identifier_state")
    }


@router.post("/continue")
async def continue_pipeline(
    thread_id: str,
    selected_columns_to_remove: list[str]
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await ml_graph.ainvoke(
        Command(
            resume=selected_columns_to_remove
        ),
        config=config
    )

    return {
        "status": "completed",
        "selected_columns": selected_columns_to_remove,
        "cleaning_plan": result.get("cleaning_plan"),
        "clean_state": result.get("cleaning_state"),
        "cleaned_file_path": result.get("cleaned_file_path")
    }