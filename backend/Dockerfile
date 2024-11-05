# Utilisation de l'image officielle Python pour FastAPI
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers et installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
