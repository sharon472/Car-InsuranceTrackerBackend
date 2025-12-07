from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

# Base class for all models
Base = declarative_base()

# 1. Engine and Session
engine = create_engine("sqlite:///car_insurance.db", echo=True)
Session = sessionmaker(bind=engine)

# Dependency for FastAPI to use DB session
def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


# 2. Models
class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    model = Column(String, nullable=False)
    assigned_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    insurance_due = Column(Date, nullable=True)
    notes = Column(String, nullable=True)

    assigned = relationship("Employee", back_populates="cars")
    insurances = relationship("Insurance", back_populates="car")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    cars = relationship("Car", back_populates="assigned")


class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    company = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Integer, nullable=True)

    car = relationship("Car", back_populates="insurances")


class UserLogin(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # for now, plaintext

