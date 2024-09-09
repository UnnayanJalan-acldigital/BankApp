from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# User routes
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/users/transfer/", response_model=schemas.TransactionCreate)
def transfer_money(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        return crud.transfer_money(db=db, transaction=transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Employee routes
@app.post("/employees/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@app.get("/employees/", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db=db)
