from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import os
from .database import SessionLocal, engine
from .models import Base, Passenger

app = FastAPI()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'input')  # Ensure this is an absolute path
CSV_FILE_PATH = os.path.join(UPLOAD_DIR, 'train.csv')

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save the uploaded file in the 'input' folder
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        # Read the CSV file
        data = pd.read_csv(file_location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")

    # Verify required columns
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV file: {column}")

    # Check for existing entries to prevent duplicates based on PassengerId
    existing_ids = {p.PassengerId for p in db.query(Passenger.PassengerId).all()}
    new_passengers = [
        Passenger(
            PassengerId=row['PassengerId'],
            Survived=row['Survived'],
            Pclass=row['Pclass'],
            Name=row['Name'],
            Sex=row['Sex'],
            Age=row['Age'],
            SibSp=row['SibSp'],
            Parch=row['Parch'],
            Ticket=row['Ticket'],
            Fare=row['Fare']
        )
        for _, row in data.iterrows() if row['PassengerId'] not in existing_ids
    ]

    # Bulk insert new passengers
    if new_passengers:
        db.bulk_save_objects(new_passengers)
        db.commit()

    return {"status": "Data uploaded successfully", "new_entries": len(new_passengers)}

@app.get("/load_csv")
def load_csv(db: Session = Depends(get_db)):
    # Print the path for debugging
    print("CSV file path:", CSV_FILE_PATH)

    # Check if the CSV file exists and is a file
    if not os.path.isfile(CSV_FILE_PATH):
        raise HTTPException(status_code=404, detail="train.csv file not found or is not a file in 'input' directory.")

    try:
        # Read the CSV file
        data = pd.read_csv(CSV_FILE_PATH)
        print(f"Data loaded from CSV:\n{data.head()}")  # Diagnostic print to check data loading
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading train.csv file: {str(e)}")

    # Verify required columns
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in train.csv file: {column}")

    # Insert data into the database, avoiding duplicates
    existing_ids = {p.PassengerId for p in db.query(Passenger.PassengerId).all()}
    new_passengers = [
        Passenger(
            PassengerId=row['PassengerId'],
            Survived=row['Survived'],
            Pclass=row['Pclass'],
            Name=row['Name'],
            Sex=row['Sex'],
            Age=row['Age'],
            SibSp=row['SibSp'],
            Parch=row['Parch'],
            Ticket=row['Ticket'],
            Fare=row['Fare']
        )
        for _, row in data.iterrows() if row['PassengerId'] not in existing_ids and not row.isnull().any()
    ]

    if new_passengers:
        db.bulk_save_objects(new_passengers)
        db.commit()
        print(f"{len(new_passengers)} new entries added.")  # Diagnostic print to check insertion count
    else:
        print("No new entries to add.")  # Diagnostic print for empty insertions

    return {"status": "Data loaded successfully from train.csv", "new_entries": len(new_passengers)}

@app.get("/passengers")
def get_passengers(survived: int = None, db: Session = Depends(get_db)):
    query = db.query(Passenger)
    if survived is not None:
        query = query.filter(Passenger.Survived == survived)
    return query.all()
