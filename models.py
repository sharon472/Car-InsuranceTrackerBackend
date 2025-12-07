# models.py - Confirmed Correct
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from typing import Generator
# NOTE: Removed unused imports: DateTime, datetime

# Base class for all models
Base = declarative_base()

# 1. Engine and Session
# NOTE: Using 'cars.db' as per your alembic.ini config
engine = create_engine("sqlite:///cars.db", echo=True) 
Session = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.close()

# 2. Models
class UserLogin(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    # DBML: Relationship User <-> Car
    cars_owned = relationship("Car", back_populates="owner") 

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    cars = relationship("Car", back_populates="assigned") 


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    model = Column(String, nullable=False)
    
    # ORIGINAL FIELDS
    assigned_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    insurance_due = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    
    # DBML ADDITIONS (Hybrid Fields)
    owner_name = Column(String(100), nullable=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) 

    # Relationships
    owner = relationship("UserLogin", back_populates="cars_owned")
    assigned = relationship("Employee", back_populates="cars")
    insurances = relationship("Insurance", back_populates="car")


class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    
    company = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Integer, nullable=True)
    
    # DBML ADDITION
    status = Column(String(20), nullable=True) 

    car = relationship("Car", back_populates="insurances")