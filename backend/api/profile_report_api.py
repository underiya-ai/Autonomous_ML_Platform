from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from service.profiling_service import generate_profile_report


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# Generate YData Profiling Report
@router.post("/generate")
async def generate_report(file_path: str):

    try:

        result = generate_profile_report(file_path)

        return {
            "message": "Profile report generated successfully",
            "report_name": result["report_name"],
            "report_path": result["report_path"],
            "report_url": f"/reports/{result['report_name']}"
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# View YData Profiling Report
@router.get("/{report_name}")
async def view_report(report_name: str):

    report_path = (
        Path("uploads/reports")
        / report_name
    )

    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return FileResponse(
        path=str(report_path),
        media_type="text/html"
    )