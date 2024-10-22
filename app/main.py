from app import employees, transactions, add_balance_route
from app import users
from fastapi import FastAPI
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(add_balance_route.router, prefix="/balance", tags=["Balance"])

@app.get("/")
def root():
    return {"message": "Bank Application Running!"}
