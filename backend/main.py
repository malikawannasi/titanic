from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from upload import upload_csv
from base import load_csv, get_passengers

# Initialize the FastAPI application
app = FastAPI()

# CORS configuration for allowed origins
origins = [
   "http://localhost:3000",  # Allow requests from the React app running on localhost:3000
    "localhost:3000"  # Allow requests from the local server on port 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted for production)
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in the request
)

# Add routes for file upload and data management
app.add_api_route("/upload", upload_csv, methods=["POST"])  # Route to upload a CSV file
app.add_api_route("/load_csv", load_csv, methods=["GET"])  # Route to load CSV data
app.add_api_route("/passengers", get_passengers, methods=["GET"])  # Route to get passengers data
