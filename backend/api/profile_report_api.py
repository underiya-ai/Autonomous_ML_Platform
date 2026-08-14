from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from service.profiling_service import generate_profile_report

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/{report_name}")
async def view_report(report_name: str):

    report_path = Path("uploads/reports") / report_name

    # Agar report already exist karti hai
    if report_path.exists():

        return FileResponse(
            path=str(report_path),
            media_type="text/html"
        )

    # Report exist nahi karti
    # Original dataset ka pth nikalenge
    file_name = report_name.replace("_profile.html", ".csv")

    file_path = Path("uploads") / file_name

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # Generate report
    result = generate_profile_report(
        str(file_path)
    )

    # Generated report return karo
    return FileResponse(
        path=result["report_path"],
        media_type="text/html"
    )