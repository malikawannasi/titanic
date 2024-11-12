from sqlalchemy import Column, Integer, String, Float
from database import Base

# Define the Passenger model, representing a row in the "passengers" table
class Passenger(Base):
    __tablename__ = "passengers"
    
    # Define columns with their data types and primary key/index configurations
    PassengerId = Column(Integer, primary_key=True, index=True)  # Primary key, indexed for faster lookups
    Survived = Column(Integer)  # Survival status (0 or 1)
    Pclass = Column(Integer)  # Passenger class (1, 2, or 3)
    Name = Column(String)  # Passenger's full name
    Sex = Column(String)  # Gender of the passenger
    Age = Column(Float)  # Age of the passenger
    SibSp = Column(Integer)  # Number of siblings/spouses aboard
    Parch = Column(Integer)  # Number of parents/children aboard
    Ticket = Column(String)  # Ticket number
    Fare = Column(Float)  # Fare paid for the ticket
