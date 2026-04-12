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


# file_service.py:
# - Bu faylda upload olunan faylların yoxlanılması və müvəqqəti saxlanılması üçün ayrıca service yaradılıb.
# - Məqsəd file handling logic-i route qatından ayırmaqdır.
# - Bu yanaşma backend-i daha modulyar edir və file-related dəyişiklikləri bir yerdən idarə etməyə imkan verir.


# I extracted file validation and temporary storage into a dedicated file service.
# This keeps the route layer cleaner and centralizes file-handling logic in one place,
# which improves maintainability and separation of concerns.