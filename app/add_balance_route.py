from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

# Route to add balance to user or employee
@router.post("/add/")
def add_balance(balance_data: schemas.AddBalance, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    if balance_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if balance_data.account_type == "user":
        user = db.query(models.User).filter(models.User.id == balance_data.account_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.balance += balance_data.amount
        db.commit()
        return {"message": f"Balance added successfully. New balance: {user.balance}"}

    elif balance_data.account_type == "employee":
        employee = db.query(models.Employee).filter(models.Employee.id == balance_data.account_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee.balance += balance_data.amount
        db.commit()
        return {"message": f"Balance added successfully. New balance: {employee.balance}"}

    else:
        raise HTTPException(status_code=400, detail="Invalid account type")
     