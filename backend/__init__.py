from .database import engine, Base
from .models import Passenger

# Crée toutes les tables dans la base de données
Base.metadata.create_all(bind=engine)
