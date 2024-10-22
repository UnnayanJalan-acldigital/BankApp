from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/transfer/")
def transfer_money(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == transaction.sender_id).first()
    employee = db.query(models.Employee).filter(models.Employee.id == transaction.receiver_id).first()

    if not user or not employee:
        raise HTTPException(status_code=400, detail="User or Employee not found")

    if user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance += transaction.amount
    employee.balance -= transaction.amount

    db.add(models.Transaction(**transaction.dict()))
    db.commit()

    return {"message": "Transfer successful"}
