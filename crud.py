from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def transfer_money(db: Session, transaction: schemas.TransactionCreate):
    sender = get_user(db, transaction.sender_id)
    receiver = get_user(db, transaction.receiver_id)

    if sender.balance >= transaction.amount:
        sender.balance -= transaction.amount
        receiver.balance += transaction.amount

        db_transaction = models.Transaction(
            sender_id=transaction.sender_id,
            receiver_id=transaction.receiver_id,
            amount=transaction.amount
        )
        db.add(db_transaction)
        db.commit()
        return db_transaction
    else:
        raise Exception("Insufficient balance")

def create_employee(db: Session, employee: schemas.EmployeeBase):
    db_employee = models.Employee(
        name=employee.name,
        department_id=employee.department_id,
        department=employee.department,
        position=employee.position,
        email=employee.email
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session):
    return db.query(models.Employee).all()
