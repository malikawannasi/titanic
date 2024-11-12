from fastapi import FastAPI
from .upload import upload_csv
from .base import load_csv, get_passengers

# Initialize the FastAPI application
app = FastAPI()

# Add routes for file upload and data management
app.add_api_route("/upload", upload_csv, methods=["POST"])
app.add_api_route("/load_csv", load_csv, methods=["GET"])
app.add_api_route("/passengers", get_passengers, methods=["GET"])

