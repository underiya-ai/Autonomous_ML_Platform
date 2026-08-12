from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from service.upload_service import save_uploaded_file
from service.profiling_service import generate_profile_report


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


# Upload + Profiling
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    # 1. Save uploaded file
    result = await save_uploaded_file(file)

    # 2. Get saved file path
    file_path = result["file_path"]

    # 3. Generate YData profiling report
    profile_result = generate_profile_report(file_path)

    # 4. Get generated HTML report name
    report_name = profile_result["report_name"]

    # 5. Return everything
    return {
        "message": "File uploaded and profiled successfully",

        "file": result,

        "profile": profile_result,

        "report_url": f"/files/report/{report_name}"
    }


# View YData HTML Report
@router.get("/report/{report_name}")
async def view_report(report_name: str):

    report_path = Path("uploads/reports") / report_name

    if not report_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return FileResponse(
        path=str(report_path),
        media_type="text/html"
    )