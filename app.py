from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from models import Car, Employee, Insurance, UserLogin, get_db
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="THE RESSEY TOURS AND CAR HIRE INSURANCE TRACKER API")

# -------------------- CORS CONFIGURATION --------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------- END CORS FIX --------------------


# -------------------- Pydantic Schemas --------------------

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

class CarSchema(BaseSchema):
    plate_number: str
    model: str
    assigned_id: Optional[int] = None
    insurance_due: Optional[str] = None
    notes: Optional[str] = None
    owner_name: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None 

class EmployeeSchema(BaseSchema):
    name: str
    role: str
    phone: Optional[str] = None
    id: Optional[int] = None

class InsuranceSchema(BaseSchema):
    car_id: int
    company: str
    start_date: str
    end_date: str
    premium: Optional[int] = None
    status: Optional[str] = None 
    id: Optional[int] = None

class UserSchema(BaseModel):
    username: str
    password: str
    id: Optional[int] = None 


# -------------------- Routes --------------------

@app.get("/")
def root():
    return {"message": "Car Insurance Tracker API running"}

# -------- Cars --------
@app.get("/cars", response_model=List[CarSchema])
def get_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()

@app.post("/cars", response_model=CarSchema)
def create_car(car: CarSchema, db: Session = Depends(get_db)):
    new_car = Car(**car.model_dump(exclude_unset=True))
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@app.put("/cars/{car_id}", response_model=CarSchema)
def update_car(car_id: int, car: CarSchema, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
        
    for key, value in car.model_dump(exclude_unset=True).items():
        setattr(db_car, key, value)
        
    db.commit()
    db.refresh(db_car)
    return db_car
    
@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found") 
    
    db.delete(db_car)
    db.commit()
    return

# -------- User Login/Registration --------

@app.post("/users", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    existing = db.query(UserLogin).filter(UserLogin.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    new_user = UserLogin(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=UserSchema)
def login_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserLogin).filter(UserLogin.username == user.username).first()
    
    if db_user is None or db_user.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return db_user

# -------------------- STARTUP EVENT (The Final Fix) --------------------

@app.on_event("startup")
def create_admin_on_startup():
    """Ensures the admin user with password '1234' exists every time the server starts."""
    db: Session
    for db in get_db():
        db_user = db.query(UserLogin).filter(UserLogin.username == "admin").first()
        
        if db_user:
            if db_user.password != "1234":
                db_user.password = "1234"
                db.commit()
                print(">>> STARTUP: Admin user password updated to '1234'.")
            else:
                print(">>> STARTUP: Admin user already exists with correct password.")
        else:
            new_user = UserLogin(username="admin", password="1234")
            db.add(new_user)
            db.commit()
            print(">>> STARTUP: Admin user 'admin' created with password '1234'.")
        return