from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

class EmployeeBase(BaseModel):
    name: str
    department_id: int
    department: str
    position: str
    email: str

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
