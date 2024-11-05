from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import os
from .database import SessionLocal, engine
from .models import Base, Passenger

app = FastAPI()
UPLOAD_DIR = './input'

# Initialisation de la base de données
Base.metadata.create_all(bind=engine)

# Dépendance de session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Enregistrer le fichier dans le dossier 'input'
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # Enregistrer le fichier
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        # Lire le fichier CSV
        data = pd.read_csv(file_location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la lecture du fichier CSV: {str(e)}")

    # Vérifiez que les colonnes attendues sont présentes dans les données
    required_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare']
    for column in required_columns:
        if column not in data.columns:
            raise HTTPException(status_code=400, detail=f"Colonne manquante dans le fichier CSV: {column}")

    # Insertion des données dans la base
    for _, row in data.iterrows():
        passenger = Passenger(
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
        db.add(passenger)

    db.commit()
    return {"status": "Data uploaded successfully"}

@app.get("/passengers")
def get_passengers(survived: int = None, db: Session = Depends(get_db)):
    query = db.query(Passenger)
    if survived is not None:
        query = query.filter(Passenger.Survived == survived)
    return query.all()
