from models import TransactionsUser, AccountUser
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated
from banking_system_validation import CreateAccountModule, DepositModule


Base = declarative_base()
session = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]




def log_transaction(account_number, trans_type, amount):
    new_user = TransactionsUser(account_number,trans_type,amount)
    session.add(new_user)
    session.commit()
    session.close()
    



def create_account(create_account_module: CreateAccountModule, db: db_dependency):
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







""" d code """
# def log_transaction(db, account_number, trans_type, amount):
#     new_user = TransactionsUser(account_number,trans_type,amount)
#     db.add(new_user)
#     db.commit()
#     db.close()
    
    

"""kal no code """
# def create_account(holder_name, account_type, balance):
#     try: 
        
#         session = connect()
#         new_user = AccountUser(holder_name,account_type,balance)
#         session.add(new_user)
#         session.commit()
        
        
#         acc_num = new_user.account_number
#         log_transaction(acc_num,'deposit',balance)
#         session.commit()
#         session.close()
#         print(f"Account created successfully Account Number: {acc_num}")
        
#     except Exception as e:
#         print(f"Error In bank_account.py (create_account): {type(e).__name__} - {e}")
        
   