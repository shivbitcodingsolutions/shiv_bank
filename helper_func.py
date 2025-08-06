from models import TransactionsUser, AccountUser
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated
from banking_system_validation import CreateAccountModule, DepositModule, WithdrawModule
from logger import setup_logger


db = SessionLocal()
logger = setup_logger()


# db function 
def get_db():
    
    """ This function connect database """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# log-transaction
def log_transaction(account_number, trans_type, amount):
    
    """ This function track all transaction and enter all details in database """
    
    try:
        logger.debug("log_transaction() get all info")
        new_user = TransactionsUser(account_number,trans_type,amount)
        db.add(new_user)
        db.commit()
        logger.debug("Log_transaction() Enter all details in database")
        db.close()
    except Exception as e:                    
        logger.error(f"Error in log_transaction() : {e}") 


# create-account
def create_acc(create_account_module: CreateAccountModule, db: db_dependency):
    
    """ This function tack all account details and create new account and also store in database"""
    
    try:
        logger.debug("All account details get by create(): [/create-account]")
        new_account = AccountUser(
            holder_name=create_account_module.holder_name,
            account_type=create_account_module.account_type,
            balance=create_account_module.initial_deposit
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        log_transaction(new_account.account_number, 'Deposit', new_account.balance)
        logger.debug("Account created successfully : [/create-account]")
        return {"Msg": "Account Created Successfully", "account_number": new_account.account_number}
    
    except Exception as e:                    
        logger.error(f"Error in create_acc() : {e}")
        




# deposit
def deposit(deposit_module : DepositModule, db: db_dependency):
    
    """ This function tack all deposit details and update account balance in database"""

    try:
        
        
        logger.debug("All deposit details get by deposit_amount(): [/deposit]")
        account_number = deposit_module.account_number
        user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
        user[0].balance = float(user[0].balance) + deposit_module.amount
        log_transaction(account_number, 'deposit', deposit_module.amount)
        db.commit()
        db.close()
        
        logger.debug("Deposit successfully : [/deposit]")
        # return {"Msg": "Deposit Successfully"}
        return JSONResponse(content={"Msg": "Deposit Successfully"}, status_code=201)
    
    except Exception as e:                    
        logger.error(f"Error in deposit() : {e}") 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


# withdraw
def withdraw(withdraw_module : WithdrawModule, db: db_dependency):
    
    """ This function tack all withdraw details and update account balance in database"""
    
    try: 
        
        logger.debug("All withdraw details get by withdraw_amount(): [/withdraw]")
        account_number = withdraw_module.account_number
        user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
        result = user[0].balance
        if result:
            if result >= withdraw_module.amount:
                user[0].balance = float(user[0].balance) - withdraw_module.amount
                log_transaction(account_number, 'withdraw', withdraw_module.amount)
                db.commit()
                db.close()
                logger.debug("Withdrawal successful [/withdraw]")
                # return {"Msg": "Withdraw Successfully"}
                return JSONResponse(content={"Msg": "Withdraw Successfully"}, status_code=status.HTTP_201_CREATED)
            else:
                logger.debug("Insufficient balance [/withdraw]")
                # return {"Msg": "Insufficient balance"}
                return JSONResponse(content={"Msg": "Insufficient balance"}, status_code=status.HTTP_400_BAD_REQUEST)
                       
        else:
            logger.error("Account not found [/withdraw]")
            # return {"Msg": "Account not found"}
            return JSONResponse(content={"Msg": "Account not found"}, status_code=status.HTTP_404_NOT_FOUND)
    
    except Exception as e: 
        logger.error(f"Error in withdraw_amount(): {e}")                   
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")  



# get-balance
def get_balance(view_balance_module : int, db: db_dependency):
    
    """ This function tack account number as input and show current balance account"""
    
    try:
        
        logger.debug("All get-balance details get by get_bal(): [/get-balance]")
        
        account_number = view_balance_module
        user = db.query(AccountUser).filter(AccountUser.account_number == account_number)
        result = user[0].balance
        db.commit()
        db.close()
        if result:
            logger.debug("Balance show to user [/get-balance]")
            return {"Your Account balance: " : result}
        else:
            logger.error("Account not found")
            return{"Msg" : "Account Not found"}
        
    except Exception as e:
        logger.error(f"Error in get_balance(): {e}") 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")   


# view-transaction-history
def view_transaction_history(view_transaction_module : int, db: db_dependency):
    
    
    """ This function tack account number as input and show current transaction history account"""
    
    try:
        
        logger.debug("All view_history details get by view_transaction(): [/view_transaction]")
        
        account_number = view_transaction_module
        hist = db.query(TransactionsUser).filter(TransactionsUser.account_number == account_number).order_by(TransactionsUser.timestamp.desc()).all()
        db.commit()
        demo_list = []
        
        if hist:
            for h in hist:
                demo_list.append(f"{h.timestamp} - {h.transaction_type} - {h.amount}")
                
            logger.debug("ALl transaction history show to user [/view_transaction]")    
            return { "Transaction History:" : demo_list}
            
        
        else:
            logger.error("No transaction history found")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found.")
            # return {"msg" : "No transactions found."}
        
        # db.close()
        
    except Exception as e:   
        logger.error(f"Error in view_transaction_history(): {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something wrong in function")
    

