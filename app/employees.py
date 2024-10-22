from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import schemas, models, auth
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import Token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a new employee
@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
     
    hashed_password = pwd_context.hash(employee.password)
    db_employee = models.Employee(name=employee.name, hashed_password=hashed_password, email=employee.email)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/me", response_model=schemas.Employee)
def read_employees_me(current_employee: models.Employee = Depends(auth.get_current_employee)):
    return current_employee

# Login route for employees
@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.email == form_data.username).first()
    if not employee or not auth.verify_password(form_data.password, employee.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = auth.create_access_token(data={"sub": employee.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Get employee's transaction history
@router.get("/{employee_id}/transactions/", response_model=list[schemas.Transaction])
def get_employee_transactions(employee_id: int, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee.transactions
