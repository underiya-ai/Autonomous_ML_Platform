from fastapi import APIRouter, UploadFile,File

from service.upload_service import save_uploaded_file

router = APIRouter(prefix="/files",tags=["Files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    result = await save_uploaded_file(file)

    return {
        "message": "File uploaded successfully",
        "data": result
    }