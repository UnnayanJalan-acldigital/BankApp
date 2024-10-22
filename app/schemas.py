from pydantic import BaseModel, Field
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TransactionBase(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float
    transaction_type: str

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float
    transaction_type: str
    
class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    email: str

class User(UserBase):
    id: int
    balance: float
    email: str
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    name: str

class EmployeeCreate(EmployeeBase):
    password: str
    email: str

class Employee(EmployeeBase):
    id: int
    balance: float
    email: str
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True

class AddBalance(BaseModel):
    account_type: str = Field(..., example="user")
    account_id: int = Field(..., example=1)
    amount: float = Field(..., gt=0, example=100.0)
