import os
import pandas as pd
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'input')

def save_file(file: UploadFile) -> str:
    """Save the uploaded file to the UPLOAD_DIR and return its path."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return file_location

def read_csv_data(file_path: str) -> pd.DataFrame:
    """Read the CSV data from the file path."""
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")
    
    return data
