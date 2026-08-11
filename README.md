# 🏦 Bank Management System

A desktop-based **Bank Management System** developed using **Python, Tkinter, and SQLite**.

The application provides a graphical interface for managing customer accounts, banking transactions, loans, fixed deposits, ATM services, administrator operations, reports, and database backup/restore functionality.

---

## ✨ Features

### 👤 Customer Management

* Create bank account
* Customer login
* View account details
* Check account balance
* Change customer PIN
* Delete account

### 💰 Banking Operations

* Deposit money
* Withdraw money
* Transfer money between accounts
* View transaction history
* Generate mini statements
* Transaction validation

### 🏧 ATM Management

* Apply for ATM card
* ATM card approval
* ATM withdrawal
* ATM balance inquiry
* ATM mini statement
* Change ATM PIN
* Block ATM card
* Unblock ATM card
* ATM transaction management
* Generate ATM receipts
* Generate PDF ATM receipts

### 💳 Loan Management

* Apply for loans
* Loan approval
* Loan calculation
* EMI calculation
* EMI payments
* Loan status management

### 🏦 Fixed Deposit Management

* Create fixed deposits
* Calculate FD interest
* View FD details
* Manage fixed deposit records

### 👨‍💼 Admin Management

* Admin authentication
* View customer information
* Search ATM cards
* View individual ATM card details
* Approve ATM cards
* Block and unblock ATM cards
* View dashboard statistics
* Generate administrative reports

### 📊 Reports

* Bank summary reports
* Transaction reports
* ATM reports
* Admin reports
* PDF report generation
* PDF ATM receipt generation

### 💾 Backup & Restore

* Database backup
* Database restore
* Banking data recovery tools

---

## 🎯 Project Objective

The objective of this project is to develop a practical desktop banking application that demonstrates how common banking operations can be managed through a user-friendly graphical interface.

The system focuses on:

* Customer account management
* Secure banking transactions
* ATM card management
* Loan and EMI management
* Fixed deposit management
* Administrative controls
* Database management
* Report generation
* Backup and restore operations

---

## 🛠️ Technologies Used

| Technology        | Purpose                            |
| ----------------- | ---------------------------------- |
| **Python**        | Main programming language          |
| **Tkinter**       | Graphical User Interface           |
| **SQLite**        | Database management                |
| **ReportLab**     | PDF report and receipt generation  |
| **File Handling** | Receipt and backup file management |
| **VS Code**       | Development environment            |

---

## 🗄️ Database

The application uses **SQLite** for storing banking information.

### Main Database Tables

```text
accounts
transactions
loans
fixed_deposits
atm_cards
```

### Accounts

Stores customer account information such as:

* Account number
* Customer name
* Account balance
* PIN

### Transactions

Stores:

* Transaction ID
* Account number
* Transaction type
* Amount
* Date and time

### Loans

Stores:

* Loan information
* Loan amount
* EMI information
* Repayment details
* Loan status

### Fixed Deposits

Stores:

* FD information
* Deposit amount
* Interest information
* FD records

### ATM Cards

Stores:

* Card ID
* Account number
* Card number
* Card type
* Expiry date
* Card status
* ATM PIN

---

## 🔐 Security & Validation

The system includes several validation and security mechanisms:

* Customer PIN verification
* ATM PIN verification
* ATM card status verification
* ATM card blocking and unblocking
* Admin authentication
* Transaction validation
* Loan approval workflow
* Account verification
* ATM transaction verification

> **Security note:** This project is intended for educational and demonstration purposes. Production banking software would require stronger security controls, encryption, secure credential storage, auditing, and regulatory compliance.

---

## 🖥️ Application Modules

The graphical interface provides access to:

```text
┌──────────────────────────────┐
│     BANK MANAGEMENT SYSTEM   │
├──────────────────────────────┤
│ Customer Management          │
│ Banking Transactions         │
│ ATM Management               │
│ Loan Management              │
│ Fixed Deposits               │
│ Admin Management             │
│ Reports                      │
│ Backup / Restore             │
└──────────────────────────────┘
```

---

## 🚀 Installation & Setup

### 1. Install Python

Install **Python 3.x** on your computer.

Check the installed version:

```bash
python --version
```

or:

```bash
py --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/misfah2005/bank-management-system.git
```

Move into the project directory:

```bash
cd bank-management-system
```

### 3. Install Dependencies

Install the required Python packages:

```bash
py -m pip install -r requirements.txt
```

If required, ReportLab can also be installed separately:

```bash
py -m pip install reportlab
```

### 4. Run the Application

```bash
py gui.py
```

The Bank Management System graphical interface will open.

---

## 📂 Project Structure

```text
bank-management-system/
│
├── gui.py
├── main.py
├── README.md
├── requirements.txt
├── admins.example.txt
├── .gitignore
│
├── tools/
│   ├── approve_atm.py
│   ├── check_accounts.py
│   ├── check_atm.py
│   ├── check_balance.py
│   ├── check_db.py
│   ├── check_fd.py
│   ├── check_notifications.py
│   ├── check_photo.py
│   ├── check_transactions.py
│   ├── fix_atm_table.py
│   ├── recover.py
│   ├── restore_db.py
│   ├── unblock_atm.py
│   └── update_atm_table.py
│
└── ...
```

### Important Files

| File                 | Purpose                                                    |
| -------------------- | ---------------------------------------------------------- |
| `gui.py`             | Main graphical user interface                              |
| `main.py`            | Core banking/database functionality                        |
| `requirements.txt`   | Python dependencies                                        |
| `admins.example.txt` | Example administrator configuration                        |
| `tools/`             | Database checking, recovery, ATM and maintenance utilities |

> Sensitive files such as administrator credentials and local database files should not be committed to GitHub.

---

## 🧾 ATM Receipt System

The ATM module supports receipt generation for transactions.

Example:

```text
BANK MANAGEMENT SYSTEM

ATM RECEIPT

Account Number : 1001
Transaction    : EMI Payment
Amount         : Rs.10000.00
Date           : 11-08-2026
Time           : 11:45 PM
Available Balance : Rs.41800.00

THANK YOU - VISIT AGAIN
```

ATM receipts can be generated as PDF documents using **ReportLab**.

---

## 📋 Project Status

| Feature                     | Status      |
| --------------------------- | ----------- |
| Customer Account Management | ✅ Completed |
| Customer Login              | ✅ Completed |
| Deposit                     | ✅ Completed |
| Withdrawal                  | ✅ Completed |
| Money Transfer              | ✅ Completed |
| Transaction History         | ✅ Completed |
| Mini Statement              | ✅ Completed |
| Loan Management             | ✅ Completed |
| EMI Management              | ✅ Completed |
| Fixed Deposit Management    | ✅ Completed |
| ATM Card Management         | ✅ Completed |
| ATM Withdrawal              | ✅ Completed |
| ATM Balance Inquiry         | ✅ Completed |
| ATM Mini Statement          | ✅ Completed |
| ATM PIN Change              | ✅ Completed |
| ATM Card Blocking           | ✅ Completed |
| ATM Card Unblocking         | ✅ Completed |
| ATM Receipt Generator       | ✅ Completed |
| ATM PDF Receipt             | ✅ Completed |
| Admin Dashboard             | ✅ Completed |
| ATM Search                  | ✅ Completed |
| ATM Card Details            | ✅ Completed |
| Admin Reports               | ✅ Completed |
| PDF Report Generation       | ✅ Completed |
| Backup / Restore            | ✅ Completed |

---

## 🔮 Future Improvements

Possible future enhancements include:

* Online banking functionality
* Email notifications
* SMS notifications
* Two-factor authentication
* Biometric authentication
* Password hashing and stronger credential security
* Cloud database integration
* REST API integration
* Mobile application
* Advanced transaction analytics
* Improved audit logging
* Role-based administrator permissions

---

## 👨‍💻 Developer

**Mohamed Misfah**

### Project

**Bank Management System**

### Development Tools

* Python
* Tkinter
* SQLite
* ReportLab
* VS Code
* Git & GitHub

---

## 📜 Conclusion

The **Bank Management System** demonstrates the practical implementation of a desktop banking application using Python, Tkinter, and SQLite.

The project covers a wide range of real-world concepts including:

* GUI development
* Database management
* Authentication
* Banking transactions
* ATM management
* Loan and EMI processing
* Fixed deposit management
* PDF report generation
* File handling
* Backup and restore operations

This project provides a strong foundation for further development into a more advanced banking platform.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**GitHub Repository:**
https://github.com/misfah2005/bank-management-system
