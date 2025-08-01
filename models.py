from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

class AccountUser(Base):
    __tablename__ = "accounts_table"

    account_number = Column(Integer, primary_key=True, index=True)
    holder_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    
    def __init__(self,holder_name, account_type, balance):
        self.holder_name = holder_name
        self.account_type = account_type
        self.balance = balance

class TransactionsUser(Base):
    __tablename__ = "transactions_table"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, ForeignKey("accounts_table.account_number"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self,account_number ,transaction_type, amount):
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now()