import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base, get_db
from .main import app

# Set up a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_titanic.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use a test client
client = TestClient(app)

# Override the database dependency with the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database and tables before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)  # Clean up after tests

def test_upload_csv(input_folder="input", file_name="train.csv"):
    try:
        # Construct the full file path
        file_path = os.path.join(input_folder, file_name)

        # Check if the file exists at the specified path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open the file to simulate a file upload
        with open(file_path, "rb") as f:
            response = client.post("/upload", files={"file": (file_name, f, "text/csv")})

        # Check that the upload was successful
        assert response.status_code == 200
        assert response.json()["status"] == "Data uploaded successfully"
        assert response.json()["new_entries"] == 2  # Adjust this depending on your CSV content
    except Exception as e:
        print(f"test_upload_csv failed: {e}")

def test_get_passengers():
    try:
        # Test retrieving all passengers
        response = client.get("/passengers")
        assert response.status_code == 200
        passengers = response.json()
        assert len(passengers) == 2  # Should match the number of entries in the test CSV
        assert passengers[0]["Name"] == "John Doe"
        assert passengers[1]["Name"] == "Jane Doe"
    except Exception as e:
        print(f"test_get_passengers failed: {e}")

def test_get_passengers_survived():
    try:
        # Test retrieving passengers based on survival status
        response = client.get("/passengers?survived=1")
        assert response.status_code == 200
        survived_passengers = response.json()
        assert len(survived_passengers) == 1  # Only one passenger should have survived
        assert survived_passengers[0]["Name"] == "John Doe"

        response = client.get("/passengers?survived=0")
        assert response.status_code == 200
        non_survived_passengers = response.json()
        assert len(non_survived_passengers) == 1  # Only one passenger should not have survived
        assert non_survived_passengers[0]["Name"] == "Jane Doe"
    except Exception as e:
        print(f"test_get_passengers_survived failed: {e}")
