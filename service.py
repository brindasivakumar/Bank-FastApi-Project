from datetime import datetime
import re

from model import Admin,User,Transaction
from data_store import userDetails, transactionHistory, adminAccount

def createHistoryId():
    return f"HIS{len(transactionHistory)+1:05}"


def createUserId():
    return f"IOB{len(userDetails)+1:05}"


def createPassword(name, dob, phoneNumber):
    initial = name[0].upper()
    year = datetime.strptime(dob, "%d/%m/%Y").year
    lastDigits = phoneNumber[-3:]
    return initial + str(year) + lastDigits


# ---------------- USER SIGNUP ----------------

def signUp():
    name = input("Enter your name\n")

    while True:
        dob = input("Enter DOB (dd/mm/yyyy)\n")
        try:
            datetime.strptime(dob, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid DOB")

    while True:
        phone = input("Enter phone number\n")
        if re.match(r'^[6-8]\d{9}$', phone):
            break
        else:
            print("Invalid phone number")

    while True:
        email = input("Enter email\n")
        if re.match(r'.+@gmail\.com$', email):
            break
        else:
            print("Invalid email")

    age = int(input("Enter age\n"))

    if age >= 18:
        accType = "Adult Account"
    else:
        accType = "Child Account"

    city = input("Enter city\n")

    userId = createUserId()
    password = createPassword(name, dob, phone)

    newUser = User(name, dob, phone, email, city, age, accType, userId, password)
    userDetails.append(newUser)

    print("User Created Successfully")
    print("User ID:", userId)
    print("Password Rule → First letter of name + birth year + last 3 digits of phone")


# ---------------- USER LOGIN ----------------

def userLogin():

    username = input("Enter UserID / Email\n")
    password = input("Enter password\n")

    for user in userDetails:

        if (user.userId == username or user.email == username) and user.password == password:

            print("Login Successful")

            while True:

                print("1.Personal Details")
                print("2.Check Balance")
                print("3.Logout")

                choice = input()

                if choice == "1":
                    print(user.__dict__)

                elif choice == "2":
                    print("Balance:", user.balance)

                elif choice == "3":
                    return

    print("Invalid login")


# ---------------- ADMIN SIGNUP ----------------

def adminSignup():
    global adminAccount

    if adminAccount is not None:
        print("Admin already exists")
        return

    name = input("Enter admin name\n")
    pan = input("Enter PAN\n")
    aadhar = input("Enter Aadhar\n")
    password = input("Create password\n")

    adminAccount = Admin(name, pan, aadhar, password)

    print("Admin created successfully")


# ---------------- ADMIN LOGIN ----------------

def adminLogin():

    global adminAccount

    if adminAccount is None:
        print("No admin found. Please create admin first")
        return

    pan = input("Enter PAN\n")
    aadhar = input("Enter Aadhar\n")
    password = input("Enter password\n")

    if pan == adminAccount.pan and aadhar == adminAccount.aadhar and password == adminAccount.password:
        print("Admin Login Successful")
        adminDashboard()
    else:
        print("Invalid admin credentials")


# ---------------- ADMIN DASHBOARD ----------------

def adminDashboard():

    while True:

        print("\n------DASHBOARD FOR ADMIN------")
        print("1.Admin Details")
        print("2.All Customers")
        print("3.Search Customer")
        print("4.Recharge")
        print("5.Withdraw")
        print("6.History")
        print("7.Logout")

        choice = input()

        if choice == "1":
            print(adminAccount.__dict__)

        elif choice == "2":
            for user in userDetails:
                print(user.userId, user.name)

        elif choice == "3":
            searchId = input("Enter Customer ID\n")

            for user in userDetails:
                if user.userId == searchId:
                    print(user.__dict__)

        elif choice == "4":
            cid = input("Enter Customer ID\n")
            amt = int(input("Enter amount\n"))

            for user in userDetails:
                if user.userId == cid:
                    user.balance += amt

                    history = Transaction(
                        createHistoryId(),
                        cid,
                        "Recharge",
                        amt,
                        "SUCCESS"
                    )

                    transactionHistory.append(history)

                    print("Recharge successful")

        elif choice == "5":
            cid = input("Enter Customer ID\n")
            amt = int(input("Enter amount\n"))

            for user in userDetails:

                if user.userId == cid:

                    if user.balance >= amt:
                        user.balance -= amt
                        status = "SUCCESS"
                        print("Withdraw successful")
                    else:
                        status = "FAILED"
                        print("Insufficient balance")

                    history = Transaction(
                        createHistoryId(),
                        cid,
                        "Withdraw",
                        amt,
                        status
                    )

                    transactionHistory.append(history)

        elif choice == "6":

            for h in transactionHistory:
                print(h.historyId, h.customerId, h.description, h.amount, h.status)

        elif choice == "7":
            return