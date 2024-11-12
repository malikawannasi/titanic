import os
import pandas as pd
from fastapi import UploadFile, HTTPException

# Define the directory for file uploads
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'input')

def save_file(file: UploadFile) -> str:
    """Save the uploaded file to the UPLOAD_DIR and return its path."""
    # Create the upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    # Define the full path for the uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    # Save the file to the specified location
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return file_location

def read_csv_data(file_path: str) -> pd.DataFrame:
    """Read the CSV data from the file path and return it as a DataFrame."""
    try:
        # Attempt to read the CSV file into a DataFrame
        data = pd.read_csv(file_path)
    except Exception as e:
        # Raise an HTTP exception if reading fails
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")
    
    return data
