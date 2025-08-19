from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

Base = declarative_base()

class Provider(Base):
    __tablename__ = "providers"
    Provider_ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Type = Column(String)
    City = Column(String)

class Receiver(Base):
    __tablename__ = "receivers"
    Receiver_ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Type = Column(String)
    City = Column(String)

class FoodListing(Base):
    __tablename__ = "food_listings"
    Food_ID = Column(Integer, primary_key=True)
    Food_Name = Column(String)
    Quantity = Column(Integer)
    Expiry_Date = Column(Date)
    Provider_ID = Column(Integer, ForeignKey("providers.Provider_ID"))
    Provider_Type = Column(String)
    Location = Column(String)
    Food_Type = Column(String)
    Meal_Type = Column(String)

    provider = relationship("Provider", backref="listings")

class Claim(Base):
    __tablename__ = "claims"
    Claim_ID = Column(Integer, primary_key=True)
    Food_ID = Column(Integer, ForeignKey("food_listings.Food_ID"))
    Receiver_ID = Column(Integer, ForeignKey("receivers.Receiver_ID"))
    Status = Column(String)
    Timestamp = Column(DateTime)

    food_listing = relationship("FoodListing", backref="claims")
    receiver = relationship("Receiver", backref="claims")
