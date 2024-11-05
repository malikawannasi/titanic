
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Passenger(Base):
    __tablename__ = "passengers"
    PassengerId = Column(Integer, primary_key=True, index=True)
    Survived = Column(Integer)
    Pclass = Column(Integer)
    Name = Column(String)
    Sex = Column(String)
    Age = Column(Float)
    SibSp = Column(Integer)
    Parch = Column(Integer) 
    Ticket = Column(String)
    Fare = Column(Float)
