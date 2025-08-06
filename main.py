from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from database import engine,Base
from sqlalchemy.orm import Session
from banking_system_validation import CreateAccountModule, DepositModule, WithdrawModule
from helper_func import create_acc, get_db, deposit, withdraw, get_balance, view_transaction_history
from logger import setup_logger
from models import AccountUser


app = FastAPI()
logger = setup_logger()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def wlc():
    logger.info("User just hit /get endpoint ")
    return {"Msg": "Welcome to Shiv Bank"}


@app.post("/create-account")
def create(account: CreateAccountModule, db: db_dependency):
     
    """ 
    Create a account endpoint and import [CreateAccountModule] class from [banking_system_validation.py] for validation 
    This function tack all account input from [CreateAccountModule] class and give to [create()] for account-create process
    """
    try:
        
        logger.debug("User just hit [/create-account] endpoint")
        
        result = account
        if result is None:
            logger.error("Account details not found while created account : [/create-account]")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account details does not found")
        
        logger.debug("Account info put on create_acc() : [/create-account]")
        return create_acc(account, db)
    
    except Exception as e:                    
        logger.error(f"Error in create(): {e}") 


@app.put("/deposit")
def deposit_amount(deposit_module : DepositModule, db: db_dependency):
    
     
    """ 
    Create a deposit endpoint and import [deposit_module] class from [banking_system_validation.py] for validation 
    This function tack all account input from [deposit_module] class and give to [deposit()] for deposit process
    """
    
    try:
        logger.debug("User just hit [/deposit] endpoint")
        
        result = deposit_module
        if result is None:
            logger.error("deposit details not found while deposit amount in account : [/deposit]")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deposit details does not found")
        
        logger.debug("Account info put on deposit() : [/deposit]")
        return deposit(deposit_module, db)
    
    except Exception as e:                    
        logger.error(f"Error in deposit_amount(): {e}") 
    
    
@app.put("/withdraw")
def withdraw_amount(withdraw_module : WithdrawModule, db: db_dependency):
    
    """ 
    Create a withdraw endpoint and import [withdraw_module] class from [banking_system_validation.py] for validation 
    This function tack all account input from [withdraw_module] class and give to [withdraw()] for withdraw process
    """
    
    try:
        
        logger.debug("User just hit [/withdraw] endpoint")
        
        result = withdraw_module
        if result is None:
            logger.error("withdraw details not found while withdraw amount in account : [/withdraw]")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Withdraw details does not found")
        
        logger.debug("Account info put on withdraw() : [/withdraw]")
        return withdraw(withdraw_module, db)
    
    except Exception as e:
        logger.error(f"Error in withdraw_amount(): {e}")                    


@app.get("/get-balance")
def get_bal(view_balance_module : int, db: db_dependency):
    
    
    """ 
    Create a get-balance endpoint and import [view_balance_module] class from [banking_system_validation.py] for validation 
    This function tack all account input from [view_balance_module] class and give to [get_balance()] for show current balance process
    """
    
    try:
        
        logger.debug("User just hit [/get-balance] endpoint")
        
        result = view_balance_module
        if result is None:
            logger.error("Account balance details not found while get-balance process : [/get-balance]")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account balance does not found")
        
        logger.debug("Account info put on get_balance() : [/get-balance]")
        return get_balance(view_balance_module, db)
    
    except Exception as e:
        logger.error(f"Error in get_bal(): {e}")  
    
   
@app.get("/view-transaction")
def view_transaction(view_transaction_module : int, db: db_dependency):
    
    """" 
    Create a view-transaction endpoint and import [view_transaction_module] class from [banking_system_validation.py] for validation 
    This function tack all account input from [view_transaction_module] class and give to [view_transaction_history()] for show current transaction_history
    """ 
    
    try:
        
        logger.debug("User just hit [/view_transaction] endpoint")
        
        result = view_transaction_module
        if result is None:
            logger.error("Account history details not found while view_transaction process : [/view_transaction]")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account history does not found")
        
        logger.debug("Account info put on view_transaction_history() : [/view-transaction]")
        return view_transaction_history(view_transaction_module, db)
    
    except Exception as e:
        logger.error(f"Error in view_transaction(): {e}")