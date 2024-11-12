from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import os
from database import get_db
from models import Passenger
from file_utils import read_csv_data

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'input', 'train.csv')

def load_csv(db: Session = Depends(get_db)):
    # Check if the CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        # Raise a FileNotFoundError with a more specific message
        raise HTTPException(status_code=404, detail=f"File not found: {CSV_FILE_PATH}. Please ensure that 'train.csv' exists in the 'input' directory.")

    try:
        # Use the utility function to read the CSV file
        data = read_csv_data(CSV_FILE_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"The file {CSV_FILE_PATH} was not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading the CSV file: {str(e)}")

    # Verify required columns
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in train.csv file: {column}")

    # Check for duplicates to avoid inserting existing data
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

    # Insert new passengers if any are found
    if new_passengers:
        db.bulk_save_objects(new_passengers)
        db.commit()

    return {"status": "Data loaded successfully from train.csv", "new_entries": len(new_passengers)}

def get_passengers(survived: int = None, db: Session = Depends(get_db)):
    # Query the database for passengers, optionally filtering by survival status
    query = db.query(Passenger)
    if survived is not None:
        query = query.filter(Passenger.Survived == survived)
    return query.all()

