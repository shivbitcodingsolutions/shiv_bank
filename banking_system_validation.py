from pydantic import BaseModel, Field
from typing import Annotated, Literal

class CreateAccountModule(BaseModel):
    holder_name: Annotated[str, Field(..., description="Enter Name of the account holder")]
    account_type: Annotated[Literal["Savings", "Current"], Field(..., description="Enter Type of account")]
    initial_deposit: Annotated[float, Field(..., description="Enter Initial Deposit Amount: ₹")]

class DepositModule(BaseModel):
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]
    amount: Annotated[float, Field(..., description="Enter Deposit Amount")]

class WithdrawModule(BaseModel):
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]
    amount: Annotated[float, Field(..., description="Enter Withdraw Amount")]
    
class ViewBalanceModule(BaseModel):
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]
    

class ViewTransactionHistoryModule(BaseModel):
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]