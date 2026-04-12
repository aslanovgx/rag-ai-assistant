import tempfile


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file temporarily and return file path.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name