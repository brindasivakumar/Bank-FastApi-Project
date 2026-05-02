# schemas.py

from pydantic import BaseModel, Field, EmailStr

from typing import Optional, List

 

# ---------- Admin ----------

class AdminSignupIn(BaseModel):

    name: str

    pan: str

    aadhar: str

    password: str

 

class AdminLoginIn(BaseModel):

    pan: str

    aadhar: str

    password: str

 

class AdminOut(BaseModel):

    name: str

    pan: str

    aadhar: str

 

# ---------- User ----------

class UserSignupIn(BaseModel):

    name: str

    dob: str = Field(..., description="Format dd/mm/yyyy")

    phoneNumber: str

    email: EmailStr

    city: str

    age: int

 

class UserOut(BaseModel):

    userId: str

    name: str

    dob: str

    phoneNumber: str

    email: EmailStr

    city: str

    age: int

    accountType: str

    balance: int

 

class UserLoginIn(BaseModel):

    username: str = Field(..., description="UserID or Email")

    password: str

 

# ---------- Transactions ----------

class RechargeIn(BaseModel):

    amount: int = Field(..., gt=0)

 

class WithdrawIn(BaseModel):

    amount: int = Field(..., gt=0)

 

class TransactionOut(BaseModel):

    historyId: str

    customerId: str

    description: str

    amount: int

    status: str