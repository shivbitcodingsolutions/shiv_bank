from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from models import AccountUser
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from banking_system_validation import CreateAccountModule, DepositModule, WithdrawModule, ViewBalanceModule
from helper_func import log_transaction, create_account

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def wlc():
    return {"Msg": "Welcome to Shiv Bank"}



@app.post("/create-account")
def create_acc(create_account_module: CreateAccountModule, db: db_dependency):
    
    new_account = AccountUser(
        holder_name=create_account_module.holder_name,
        account_type=create_account_module.account_type,
        balance=create_account_module.initial_deposit
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    log_transaction(new_account.account_number, 'Deposit', new_account.balance)
    return {"Msg": "Account Created Successfully", "account_number": new_account.account_number}


@app.put("/deposit")
def deposit(deposit_module : DepositModule, db: db_dependency):

    account_number = deposit_module.account_number
    user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
    user[0].balance = float(user[0].balance) + deposit_module.amount
    log_transaction(account_number, 'deposit', deposit_module.amount)
    db.commit()
    db.close()
    return {"Msg": "Deposit Successfully"}
    


@app.put("/withdraw")
def withdraw(withdraw_module : WithdrawModule, db: db_dependency):
    
    account_number = withdraw_module.account_number
    user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
    result = user[0].balance
    if result:
        if result >= withdraw_module.amount:
            user[0].balance = float(user[0].balance) - withdraw_module.amount
            log_transaction(account_number, 'withdraw', withdraw_module.amount)
            db.commit()
            print("Withdrawal successful")
        else:
            print("Insufficient balance")    
    else:
        print("Account not found")
    db.close()
    return {"Msg": "Withdraw Successfully"}
    

@app.get("/get-balance")
def get_balance(view_balance_module : int, db: db_dependency):
    
    account_number = view_balance_module
    user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
    result = user[0].balance
    db.commit()
    if result:
        return {"Your Account balance: " : result}
    else:
        print({"Msg" : "Account Not found"})
    db.close()
    
# @app.post("/get-balance")
# def get_balance(view_balance_module : ViewBalanceModule, db: db_dependency):
    
#     account_number = view_balance_module.account_number
#     user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
#     result = user[0].balance
#     db.commit()
#     if result:
#         return {"Your Account balance: " : result}
#     else:
#         print({"Msg" : "Account Not found"})
#     db.close()












