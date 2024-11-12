from fastapi import UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Passenger
from .file_utils import save_file, read_csv_data

async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded file in the 'input' folder using the save_file function
    file_location = save_file(file)
    
    # Read the CSV file using the read_csv_data function
    data = read_csv_data(file_location)

    # Check for required columns
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV file: {column}")

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
        for _, row in data.iterrows() if row['PassengerId'] not in existing_ids
    ]

    # Bulk insert the new passengers
    if new_passengers:
        db.bulk_save_objects(new_passengers)
        db.commit()

    return {"status": "Data uploaded successfully", "new_entries": len(new_passengers)}
