from pathlib import Path
from fastapi import UploadFile,HTTPException


UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".csv"
    
}

async def save_uploaded_file(file: UploadFile) -> dict:

    if not file.filename:
        raise HTTPException(status_code=400,detail="file name is missing")

    extension = Path(file.filename).suffix.lower()

    # validate the extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400,detail="Only CSV file are allowed"
        )

    # create file apth
    file_path = UPLOAD_DIR / file.filename

    # save file 
    with open(file_path, "wb") as f:

        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    return {
        "filename":file.filename,
        "file_type": extension,
        "file_path": str(file_path)
        
    }
