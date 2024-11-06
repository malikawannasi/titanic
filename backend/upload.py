from fastapi import UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import pandas as pd
from .database import get_db
from .models import Passenger

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'input')  # Assurez-vous que ce soit un chemin absolu

async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Sauvegarde du fichier téléchargé dans le dossier 'input'
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        # Lire le fichier CSV
        data = pd.read_csv(file_location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")

    # Vérifier les colonnes nécessaires
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV file: {column}")

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
        for _, row in data.iterrows() if row['PassengerId'] not in existing_ids
    ]

    # Insertion en masse des nouveaux passagers
    if new_passengers:
        db.bulk_save_objects(new_passengers)
        db.commit()

    return {"status": "Data uploaded successfully", "new_entries": len(new_passengers)}

