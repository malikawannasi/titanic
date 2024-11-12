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

def test_upload_csv():
    # Sample CSV content to test uploading
    csv_content = (
        "PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare\n"
        "1,1,1,John Doe,male,22,1,0,A/5 21171,71.2833\n"
        "2,0,3,Jane Doe,female,38,1,0,PC 17599,53.1000\n"
    )

    # Save the content to a temporary file
    with open("test_upload.csv", "w") as f:
        f.write(csv_content)

    # Open the file to simulate a file upload
    with open("test_upload.csv", "rb") as f:
        response = client.post("/upload", files={"file": ("test_upload.csv", f, "text/csv")})

    os.remove("test_upload.csv")  # Clean up the temporary file

    # Check that the upload was successful
    assert response.status_code == 200
    assert response.json()["status"] == "Data uploaded successfully"
    assert response.json()["new_entries"] == 2  # Two entries in the CSV

def test_get_passengers():
    # Test retrieving all passengers
    response = client.get("/passengers")
    assert response.status_code == 200
    passengers = response.json()
    assert len(passengers) == 2  # Should match the number of entries in the test CSV
    assert passengers[0]["Name"] == "John Doe"
    assert passengers[1]["Name"] == "Jane Doe"

def test_get_passengers_survived():
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
