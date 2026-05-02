# main.py
#To run
#pip install -r requirements.txt
#pip install email-validator
#uvicorn main:app --reload


from fastapi import FastAPI, HTTPException

from typing import List, Optional

 

from model import Admin, User, Transaction

from data_store import adminAccount, userDetails, transactionHistory

from schemas import (

    AdminSignupIn, AdminLoginIn, AdminOut,

    UserSignupIn, UserOut, UserLoginIn,

    RechargeIn, WithdrawIn, TransactionOut

)

from utils import create_history_id, create_user_id, create_password

 

app = FastAPI(title="Indian Overseas Bank API", version="1.0.0")

 

# ---------------------- ADMIN ----------------------

 

@app.post("/admin/signup", response_model=AdminOut, tags=["Admin"])

def admin_signup(payload: AdminSignupIn):

    global adminAccount

    if adminAccount is not None:

        raise HTTPException(status_code=400, detail="Admin already exists")

    adminAccount = Admin(

        name=payload.name,

        pan=payload.pan,

        aadhar=payload.aadhar,

        password=payload.password

    )

    return AdminOut(name=adminAccount.name, pan=adminAccount.pan, aadhar=adminAccount.aadhar)

 

@app.post("/admin/login", tags=["Admin"])

def admin_login(payload: AdminLoginIn):

    if adminAccount is None:

        raise HTTPException(status_code=404, detail="No admin found. Please create admin first.")

    if payload.pan == adminAccount.pan and payload.aadhar == adminAccount.aadhar and payload.password == adminAccount.password:

        return {"message": "Admin login successful"}

    raise HTTPException(status_code=401, detail="Invalid admin credentials")

 

# ---------------------- USERS ----------------------

 

@app.post("/users", response_model=UserOut, tags=["Users"])

def user_signup(payload: UserSignupIn):

    # simple validations (mirrors your CLI version)

    import re

    from datetime import datetime

 

    # DOB format validate

    try:

        datetime.strptime(payload.dob, "%d/%m/%Y")

    except ValueError:

        raise HTTPException(status_code=400, detail="Invalid DOB format. Use dd/mm/yyyy")

 

    # phone validate

    if not re.match(r'^[6-9]\d{9}$', payload.phoneNumber):

        raise HTTPException(status_code=400, detail="Invalid phone number")

 

    # age -> account type

    accType = "Adult Account" if payload.age >= 18 else "Child Account"

 

    # duplicate email or phone check (optional)

    for u in userDetails:

        if u.email == payload.email:

            raise HTTPException(status_code=400, detail="Email already exists")

        if u.phoneNumber == payload.phoneNumber:

            raise HTTPException(status_code=400, detail="Phone already exists")

 

    userId = create_user_id()

    password = create_password(payload.name, payload.dob, payload.phoneNumber)

    u = User(

        name=payload.name,

        dob=payload.dob,

        phoneNumber=payload.phoneNumber,

        email=payload.email,

        city=payload.city,

        age=payload.age,

        accountType=accType,

        userId=userId,

        password=password

    )

    userDetails.append(u)

 

    return UserOut(

        userId=u.userId, name=u.name, dob=u.dob, phoneNumber=u.phoneNumber,

        email=u.email, city=u.city, age=u.age, accountType=u.accountType, balance=u.balance

    )

 

@app.post("/auth/login", tags=["Users"])

def user_login(payload: UserLoginIn):

    # username can be userId or email

    for u in userDetails:

        if (u.userId == payload.username or u.email == payload.username) and u.password == payload.password:

            return {"message": "Login successful", "userId": u.userId, "name": u.name}

    raise HTTPException(status_code=401, detail="Invalid credentials")

 

@app.get("/users", response_model=List[UserOut], tags=["Users"])

def list_users():

    return [

        UserOut(

            userId=u.userId, name=u.name, dob=u.dob, phoneNumber=u.phoneNumber,

            email=u.email, city=u.city, age=u.age, accountType=u.accountType, balance=u.balance

        )

        for u in userDetails

    ]

 

@app.get("/users/{user_id}", response_model=UserOut, tags=["Users"])

def get_user(user_id: str):

    for u in userDetails:

        if u.userId == user_id:

            return UserOut(

                userId=u.userId, name=u.name, dob=u.dob, phoneNumber=u.phoneNumber,

                email=u.email, city=u.city, age=u.age, accountType=u.accountType, balance=u.balance

            )

    raise HTTPException(status_code=404, detail="User not found")

 

# ---------------------- ADMIN ACTIONS ----------------------

 

@app.put("/admin/users/{user_id}/recharge", tags=["Admin"])

def recharge(user_id: str, payload: RechargeIn):

    # (Optionally check admin is logged in via auth — skipped for simplicity)

    for u in userDetails:

        if u.userId == user_id:

            u.balance += payload.amount

            h = Transaction(create_history_id(), user_id, "Recharge", payload.amount, "SUCCESS")

            transactionHistory.append(h)

            return {"message": "Recharge successful", "balance": u.balance}

    raise HTTPException(status_code=404, detail="User not found")

 

@app.put("/admin/users/{user_id}/withdraw", tags=["Admin"])

def withdraw(user_id: str, payload: WithdrawIn):

    for u in userDetails:

        if u.userId == user_id:

            if u.balance >= payload.amount:

                u.balance -= payload.amount

                status = "SUCCESS"

                msg = "Withdraw successful"

            else:

                status = "FAILED"

                msg = "Insufficient balance"

            h = Transaction(create_history_id(), user_id, "Withdraw", payload.amount, status)

            transactionHistory.append(h)

            if status == "FAILED":

                raise HTTPException(status_code=400, detail=msg)

            return {"message": msg, "balance": u.balance}

    raise HTTPException(status_code=404, detail="User not found")

 

# ---------------------- TRANSACTIONS ----------------------

 

@app.get("/transactions", response_model=List[TransactionOut], tags=["Transactions"])

def list_transactions():

    return [

        TransactionOut(

            historyId=t.historyId,

            customerId=t.customerId,

            description=t.description,

            amount=t.amount,

            status=t.status

        ) for t in transactionHistory

    ]

 

@app.get("/users/{user_id}/transactions", response_model=List[TransactionOut], tags=["Transactions"])

def user_transactions(user_id: str):

    # ensure user exists

    if not any(u.userId == user_id for u in userDetails):

        raise HTTPException(status_code=404, detail="User not found")

    return [

        TransactionOut(

            historyId=t.historyId,

            customerId=t.customerId,

            description=t.description,

            amount=t.amount,

            status=t.status

        )

        for t in transactionHistory if t.customerId == user_id

    ]

