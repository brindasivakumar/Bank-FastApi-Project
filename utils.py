# utils.py

from datetime import datetime

from data_store import transactionHistory, userDetails

 

def create_history_id():

    return f"HIS{len(transactionHistory)+1:05}"

 

def create_user_id():

    return f"IOB{len(userDetails)+1:05}"

 

def create_password(name: str, dob: str, phoneNumber: str) -> str:

    initial = name[0].upper()

    year = datetime.strptime(dob, "%d/%m/%Y").year

    last_digits = phoneNumber[-3:]

    return f"{initial}{year}{last_digits}"

 