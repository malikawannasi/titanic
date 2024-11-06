from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import os
import pandas as pd
from .database import get_db
from .models import Passenger

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'input', 'train.csv')

def load_csv(db: Session = Depends(get_db)):
    # Vérifier que le fichier CSV existe
    if not os.path.isfile(CSV_FILE_PATH):
        raise HTTPException(status_code=404, detail="train.csv file not found or is not a file in 'input' directory.")

    try:
        # Lire le fichier CSV
        data = pd.read_csv(CSV_FILE_PATH)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading train.csv file: {str(e)}")

    # Vérifier les colonnes nécessaires
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in train.csv file: {column}")

    # Vérifier les doublons pour éviter d'insérer des données existantes
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

    return {"status": "Data loaded successfully from train.csv", "new_entries": len(new_passengers)}

def get_passengers(survived: int = None, db: Session = Depends(get_db)):
    query = db.query(Passenger)
    if survived is not None:
        query = query.filter(Passenger.Survived == survived)
    return query.all()
