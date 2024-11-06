from fastapi import UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Passenger
from .file_utils import save_file, read_csv_data

async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Sauvegarde du fichier téléchargé dans le dossier 'input' en utilisant la fonction save_file
    file_location = save_file(file)
    
    # Lire le fichier CSV en utilisant la fonction read_csv_data
    data = read_csv_data(file_location)

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

