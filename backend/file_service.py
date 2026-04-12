import os
import tempfile

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def save_uploaded_temp_file(file: UploadFile):
    """
    Validate the uploaded file and save it temporarily on disk.
    Returns filename, extension, and temp file path.
    """
    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF and DOCX are allowed."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
        content = file.file.read()
        tmp_file.write(content)
        temp_path = tmp_file.name

    return filename, extension, temp_path