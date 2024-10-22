from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users' 
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100))
    balance = Column(Float, default=0.0)
    
    transactions = relationship("Transaction", back_populates="user")

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(100))
    balance = Column(Float, default=0.0)
    
    transactions = relationship("Transaction", back_populates="employee")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('employees.id'))
    amount = Column(Float)
    transaction_type = Column(String(20))  
    
    user = relationship("User", back_populates="transactions")
    employee = relationship("Employee", back_populates="transactions")
