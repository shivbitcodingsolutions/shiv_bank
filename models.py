from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime


#AccountUser
class AccountUser(Base):
    
    """
    This is a class for Account user on banking system

    Attributes:
        account_number (int): Account number of user
        holder_name (str)   : Account holder name
        account_type (str)  : User Account type 
        balance (float)     : User account balance
    """
    
    
    __tablename__ = "accounts_table"

    account_number = Column(Integer, primary_key=True, index=True)
    holder_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    
    
    def __init__(self,holder_name, account_type, balance):
        
        
        """
        
        Initializes an account user object.

        Parameters:
            holder_name (str)   : Account holder name
            account_type (str)  : User Account type 
            balance (float)     : User account balance
        
        """
        
        self.holder_name = holder_name
        self.account_type = account_type
        self.balance = balance





# TransactionsUser
class TransactionsUser(Base):
    
    
    """
    This is a class for User Transactions on banking system

    Attributes:
        transaction_id (int)    : transaction number of user
        account_number (int)    : Account number of user
        transaction_type (str)  : User transaction type 
        amount  (float) :       : transaction amount
        timestamp (datetime)    : User transaction date and time
    """
    
    __tablename__ = "transactions_table"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, ForeignKey("accounts_table.account_number"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self,account_number ,transaction_type, amount):
        
        """
        Initializes an user Transaction object.
        
        Parameters:
            account_number (int)    : Account number of user
            transaction_type (str)  : User transaction type 
            amount  (float) :       : transaction amount
            timestamp (datetime)    : User transaction date and time

        """
        
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now()