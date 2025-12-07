from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from models import Car, Employee, Insurance, UserLogin, get_db

app = FastAPI()

# -------------------- Pydantic Schemas --------------------
class CarSchema(BaseModel):
    plate_number: str
    model: str
    assigned_id: Optional[int] = None
    insurance_due: Optional[str] = None
    notes: Optional[str] = None

class EmployeeSchema(BaseModel):
    name: str
    role: str
    phone: Optional[str] = None

class InsuranceSchema(BaseModel):
    car_id: int
    company: str
    start_date: str
    end_date: str
    premium: Optional[int] = None

class UserSchema(BaseModel):
    username: str
    password: str

# -------------------- Routes --------------------

# Root
@app.get("/")
def root():
    return {"message": "Car Insurance Tracker API running"}

# -------- Cars --------
@app.get("/cars", response_model=List[CarSchema])
def get_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()

@app.post("/cars", response_model=CarSchema)
def create_car(car: CarSchema, db: Session = Depends(get_db)):
    new_car = Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

# -------- Employees --------
@app.get("/employees", response_model=List[EmployeeSchema])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@app.post("/employees", response_model=EmployeeSchema)
def create_employee(emp: EmployeeSchema, db: Session = Depends(get_db)):
    new_emp = Employee(**emp.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

# -------- Insurance --------
@app.get("/insurances", response_model=List[InsuranceSchema])
def get_insurances(db: Session = Depends(get_db)):
    return db.query(Insurance).all()

@app.post("/insurances", response_model=InsuranceSchema)
def create_insurance(ins: InsuranceSchema, db: Session = Depends(get_db)):
    new_ins = Insurance(**ins.dict())
    db.add(new_ins)
    db.commit()
    db.refresh(new_ins)
    return new_ins

# -------- User Login --------
@app.post("/users", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    existing = db.query(UserLogin).filter(UserLogin.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = UserLogin(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
