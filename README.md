# 🏦 Bank Management System

A desktop-based **Bank Management System** developed using Python, Tkinter, and SQLite.
The system provides customer banking operations, ATM services, loan management, fixed deposits, transactions, and administrator controls through a graphical user interface.

---

## 🎯 Project Objective

The main objective of this project is to develop a simple and secure banking application that can manage customer accounts and provide common banking services through an easy-to-use GUI.

### Main Objectives

* Manage customer bank accounts
* Deposit and withdraw money
* Transfer money between accounts
* Check account balance
* Manage transactions
* Manage loans and EMI payments
* Manage fixed deposits
* Apply and manage ATM cards
* Perform ATM withdrawals
* Change ATM PIN
* Block and unblock ATM cards
* Generate ATM receipts
* Provide administrator controls
* Generate banking reports
* Backup and restore banking data

---

## 🛠️ Technologies Used

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| Python        | Main programming language     |
| Tkinter       | Graphical User Interface      |
| SQLite        | Database management           |
| ReportLab     | PDF report/receipt generation |
| File Handling | Backup and receipt storage    |

---

## 📌 Main Modules

### 👤 Customer Management

* Create bank account
* Customer login
* View account details
* Check account balance
* Change PIN
* Delete account

### 💰 Banking Transactions

* Deposit money
* Withdraw money
* Transfer money
* View transaction history
* Mini statement

### 🏧 ATM Management

* Apply for ATM card
* ATM card approval
* ATM withdrawal
* ATM balance inquiry
* ATM mini statement
* Change ATM PIN
* Block ATM card
* Unblock ATM card
* Generate ATM receipt
* ATM transaction management

### 💳 Loan Management

* Apply for loan
* Loan approval
* Loan calculation
* EMI calculation
* EMI payment
* Loan status management

### 🏦 Fixed Deposit

* Create fixed deposit
* Calculate FD interest
* View fixed deposit details
* Manage FD records

### 👨‍💼 Admin Management

* Admin login
* View customers
* Search ATM cards
* View individual ATM card details
* Approve ATM cards
* Block/unblock cards
* View dashboard statistics
* View bank reports

### 📊 Reports

* Bank summary report
* Transaction reports
* Admin reports
* ATM reports
* PDF report generation
* ATM receipt generation

### 💾 Backup & Restore

* Database backup
* Database restore
* Banking data protection

---

## 🗄️ Database

The application uses **SQLite** as the database.

### Main Tables

```text
accounts
transactions
loans
fixed_deposits
atm_cards
```

### Accounts Table

Stores customer bank account information such as:

* Account number
* Customer name
* Balance
* PIN

### Transactions Table

Stores:

* Transaction ID
* Account number
* Transaction type
* Amount
* Date and time

### Loans Table

Stores customer loan information and repayment details.

### Fixed Deposits Table

Stores fixed deposit information and interest-related data.

### ATM Cards Table

Stores:

* Card ID
* Account number
* Card number
* Card type
* Expiry date
* Card status
* ATM PIN

---

## 🔐 Security Features

The system includes several security mechanisms:

* Customer PIN verification
* ATM PIN verification
* ATM card status verification
* Failed ATM attempt protection
* ATM card blocking
* ATM card unblocking
* Admin authentication
* Loan approval process
* Transaction validation

---

## 🖥️ Application Interface

The system provides a graphical interface using Tkinter.

The application contains separate functions for:

```text
Customer
Admin
Banking
Loans
Fixed Deposits
ATM
Reports
Backup / Restore
```

---

## 🚀 How to Run

### 1. Install Python

Install Python 3.x on the computer.

Check the installed version:

```bash
python --version
```

or:

```bash
py --version
```

### 2. Open the Project Folder

Open the project folder in VS Code.

### 3. Install Required Package

Install ReportLab:

```bash
pip install reportlab
```

### 4. Run the Application

```bash
py gui.py
```

The Bank Management System GUI will open.

---

## 📂 Project Structure

```text
bank_management_system/
│
├── bank.py/
│   ├── gui.py
│   ├── main.py
│   ├── bank.db
│   ├── check_db.py
│   ├── check_atm.py
│   ├── check_transactions.py
│   └── check_fd.py
│
├── README.md
└── requirements.txt
```

> Keep a separate backup copy of `bank.db` before making major changes to the project.

---

## 📋 System Features

| Feature                     | Status      |
| --------------------------- | ----------- |
| Customer Account Management | ✅ Completed |
| Deposit                     | ✅ Completed |
| Withdrawal                  | ✅ Completed |
| Money Transfer              | ✅ Completed |
| Transaction History         | ✅ Completed |
| Mini Statement              | ✅ Completed |
| Loan Management             | ✅ Completed |
| EMI Management              | ✅ Completed |
| Fixed Deposit               | ✅ Completed |
| ATM Card Management         | ✅ Completed |
| ATM Withdrawal              | ✅ Completed |
| ATM Balance Inquiry         | ✅ Completed |
| ATM Mini Statement          | ✅ Completed |
| ATM PIN Change              | ✅ Completed |
| ATM Card Blocking           | ✅ Completed |
| ATM Receipt Generator       | ✅ Completed |
| Admin Dashboard             | ✅ Completed |
| ATM Search                  | ✅ Completed |
| ATM Card Details            | ✅ Completed |
| Reports                     | ✅ Completed |
| Backup / Restore            | ✅ Completed |

---

## 👨‍💻 Developer

**Mohamed Misfah**

### Project

**Bank Management System**

### Development Tools

* Python
* VS Code
* SQLite
* Tkinter
* ReportLab

---

## 📜 Conclusion

The Bank Management System provides a complete desktop-based solution for handling common banking operations.

The project demonstrates practical implementation of:

* Python programming
* Object-oriented programming concepts
* GUI development
* Database management
* File handling
* Authentication
* Transaction processing
* ATM management
* Report generation

This project can be further enhanced by adding online banking, email/SMS notifications, biometric authentication, cloud database support, and mobile application integration.
