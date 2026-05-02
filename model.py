class Admin:
    def __init__(self, name, pan, aadhar, password):
        self.name = name
        self.pan = pan
        self.aadhar = aadhar
        self.password = password


class User:
    def __init__(self, name, dob, phoneNumber, email, city, age, accountType, userId, password):
        self.name = name
        self.dob = dob
        self.phoneNumber = phoneNumber
        self.email = email
        self.city = city
        self.age = age
        self.accountType = accountType
        self.userId = userId
        self.password = password
        self.balance = 0


class Transaction:
    def __init__(self, historyId, customerId, description, amount, status):
        self.historyId = historyId
        self.customerId = customerId
        self.description = description
        self.amount = amount
        self.status = status