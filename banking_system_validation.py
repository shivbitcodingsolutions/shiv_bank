from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Literal

class CreateAccountModule(BaseModel):
    
    """ 
    This class demonstrates account input details.
    It is a pydantic class for validation.
    """
    
    holder_name: Annotated[str, Field(...,min_length=2, description="Enter Name of the account holder")]
    account_type: Annotated[Literal["Savings", "Current"], Field(..., description="Enter Type of account")]
    initial_deposit: Annotated[float, Field(..., gt=0, description="Enter Initial Deposit Amount: ₹")]
    
    @field_validator('holder_name')
    def name_must_not_be_empty_or_numeric(cls, v):
        if not v.strip(): 
            raise ValueError('Name cannot be empty')
        if v.isdigit(): 
            raise ValueError('Name cannot be a number')
        return v

class DepositModule(BaseModel):
    
    """ 
    This class demonstrates deposit details like account_number and amount.
    It is a pydantic class for validation.
    """
    
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]
    amount: Annotated[float, Field(..., gt=0, description="Enter Deposit Amount")]
    
class WithdrawModule(BaseModel):
    
    """ 
    This class demonstrates withdraw details like account_number and amount.
    It is a pydantic class for validation.
    """
    
    account_number: Annotated[int, Field(..., description="Enter Your Account Number", example=1)]
    amount: Annotated[float, Field(..., gt=0, description="Enter Withdraw Amount")]
    

