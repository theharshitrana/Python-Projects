import json
import os
import re
from datetime import datetime
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from typing import Optional, List

DATA_FILE = 'bank_gui_data.json'
ADMIN_PIN = "admin123"  # Simple admin access (in real app, use proper authentication)

class Transaction:
    def __init__(self, txn_type: str, amount: float, date: Optional[str] = None, description: str = ""):
        self.txn_type = txn_type
        self.amount = amount
        self.date = date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.description = description

    def to_dict(self):
        return {
            'txn_type': self.txn_type,
            'amount': self.amount,
            'date': self.date,
            'description': self.description
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data['txn_type'],
            data['amount'],
            data['date'],
            data.get('description', "")
        )

class BankAccount:
    def __init__(self, name, account_number, pin, account_type, balance=0.0, transactions=None):
        self.name = name
        self.account_number = account_number
        self.pin = pin
        self.account_type = account_type
        self.balance = balance
        self.transactions = transactions or []
        self.creation_date = datetime.now().strftime('%Y-%m-%d')
        self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def deposit(self, amount: float, description: str = ""):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(Transaction("deposit", amount, description=description))
        self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def withdraw(self, amount: float, description: str = ""):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transactions.append(Transaction("withdraw", amount, description=description))
        self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def apply_interest(self, rate: float = 0.04):
        if self.account_type.lower() == "savings":
            interest = self.balance * rate
            self.balance += interest
            self.transactions.append(
                Transaction("interest", interest, description=f"Interest @ {rate*100}%")
            )
            self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return interest
        return 0

    def transfer(self, target_account, amount: float, description: str = ""):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if self.account_number == target_account.account_number:
            raise ValueError("Cannot transfer to the same account")
        self.withdraw(amount, description=f"Transfer to {target_account.account_number}: {description}")
        target_account.deposit(amount, description=f"Transfer from {self.account_number}: {description}")
        self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        target_account.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_summary(self):
        return (
            f"Account Holder: {self.name}\n"
            f"Account Number: {self.account_number}\n"
            f"Account Type: {self.account_type.capitalize()}\n"
            f"Creation Date: {self.creation_date}\n"
            f"Last Accessed: {self.last_accessed}\n"
            f"Current Balance: ₹{self.balance:.2f}\n"
            f"Transaction Count: {len(self.transactions)}"
        )

    def get_transactions(self, limit=None, txn_type=None):
        transactions = self.transactions.copy()
        if txn_type:
            transactions = [t for t in transactions if t.txn_type == txn_type]
        if limit:
            transactions = transactions[-limit:]
        return transactions

    def get_balance_history(self):
        balance = 0
        history = []
        for txn in self.transactions:
            if txn.txn_type in ["deposit", "interest", "transfer_from"]:
                balance += txn.amount
            else:
                balance -= txn.amount
            history.append((txn.date, balance))
        return history

    def change_pin(self, new_pin):
        if not re.match(r'^\d{4}$', new_pin):
            raise ValueError("PIN must be 4 digits")
        self.pin = new_pin
        self.last_accessed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            'name': self.name,
            'account_number': self.account_number,
            'pin': self.pin,
            'account_type': self.account_type,
            'balance': self.balance,
            'transactions': [t.to_dict() for t in self.transactions],
            'creation_date': self.creation_date,
            'last_accessed': self.last_accessed
        }

    @staticmethod
    def from_dict(data):
        account = BankAccount(
            data['name'],
            data['account_number'],
            data['pin'],
            data['account_type'],
            data['balance'],
            [Transaction.from_dict(t) for t in data.get('transactions', [])]
        )
        account.creation_date = data.get('creation_date', datetime.now().strftime('%Y-%m-%d'))
        account.last_accessed = data.get('last_accessed', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return account

def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                raw = json.load(f)
                return {k: BankAccount.from_dict(v) for k, v in raw.items()}
            except json.JSONDecodeError:
                return {}
    return {}

def save_accounts(accounts):
    with open(DATA_FILE, 'w') as f:
        json.dump({k: acc.to_dict() for k, acc in accounts.items()}, f, indent=4)

accounts = load_accounts()
current_user = None  # Global variable declaration

# Main Application
class SmartBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBank Interface")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f2f5")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        self.update_welcome_message()
        
    def configure_styles(self):
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#2c3e50')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Primary.TButton', foreground='white', background='#3498db')
        self.style.configure('Success.TButton', foreground='white', background='#2ecc71')
        self.style.configure('Danger.TButton', foreground='white', background='#e74c3c')
        self.style.configure('Warning.TButton', foreground='white', background='#f39c12')
        
    def create_widgets(self):
        # Header
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(pady=(10, 20), fill=X)
        
        self.bank_title = ttk.Label(
            self.header_frame,
            text="🏦 SmartBank Central System",
            style='Header.TLabel'
        )
        self.bank_title.pack()
        
        self.welcome_label = ttk.Label(
            self.header_frame,
            text="",
            font=('Segoe UI', 11)
        )
        self.welcome_label.pack(pady=(5, 0))
        
        # Button Grid
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        self.buttons = [
            ("Create Account", self.create_account_gui, 'Primary.TButton'),
            ("Login", self.login_gui, 'Primary.TButton'),
            ("Deposit", self.deposit_gui, 'Success.TButton'),
            ("Withdraw", self.withdraw_gui, 'Danger.TButton'),
            ("Transfer", self.transfer_gui, 'Warning.TButton'),
            ("Apply Interest", self.interest_gui, 'Success.TButton'),
            ("Account Summary", self.summary_gui, 'Primary.TButton'),
            ("Transactions", self.transactions_gui, 'Primary.TButton'),
            ("Change PIN", self.change_pin_gui, 'Warning.TButton'),
            ("Balance History", self.show_balance_history, 'Primary.TButton'),
            ("Admin Tools", self.admin_tools_gui, 'Danger.TButton'),
            ("Logout", self.logout, 'Danger.TButton')
        ]
        
        for i, (text, command, style) in enumerate(self.buttons):
            btn = ttk.Button(
                self.button_frame,
                text=text,
                command=command,
                style=style,
                width=20
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Output Area
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.output = Text(
            self.output_frame,
            height=15,
            width=100,
            font=('Consolas', 10),
            wrap=WORD,
            state=DISABLED
        )
        self.output.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.output_frame, orient=VERTICAL, command=self.output.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.output.config(yscrollcommand=self.scrollbar.set)
        
        # Footer
        self.footer = ttk.Label(
            self.root,
            text="© 2025 SmartBank. All rights reserved.",
            font=('Segoe UI', 9),
            foreground='#7f8c8d'
        )
        self.footer.pack(side=BOTTOM, pady=5)
    
    def update_welcome_message(self):
        global current_user
        if current_user:
            self.welcome_label.config(text=f"Welcome, {current_user.name} (Account: {current_user.account_number})")
        else:
            self.welcome_label.config(text="Please login to access your account")
    
    def show_output(self, msg, clear=True):
        self.output.config(state=NORMAL)
        if clear:
            self.output.delete(1.0, END)
        self.output.insert(END, msg + "\n")
        self.output.config(state=DISABLED)
        self.output.see(END)
    
    def clear_output(self):
        self.output.config(state=NORMAL)
        self.output.delete(1.0, END)
        self.output.config(state=DISABLED)
    
    # Account Management Functions
    def create_account_gui(self):
        top = Toplevel(self.root)
        top.title("Create Account")
        top.geometry("400x400")
        top.resizable(False, False)
        
        fields = [
            ("Name:", Entry(top)),
            ("Age:", Entry(top)),
            ("Account Number:", Entry(top)),
            ("PIN (4-digit):", Entry(top, show='*')),
            ("Confirm PIN:", Entry(top, show='*')),
            ("Account Type (savings/current):", Entry(top))
        ]
        
        for i, (label_text, entry) in enumerate(fields):
            ttk.Label(top, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry.grid(row=i, column=1, padx=10, pady=5)
        
        def save_account():
            try:
                name = fields[0][1].get().strip()
                age = fields[1][1].get().strip()
                acc_no = fields[2][1].get().strip()
                pin = fields[3][1].get().strip()
                confirm_pin = fields[4][1].get().strip()
                acc_type = fields[5][1].get().strip().lower()
                
                if not name or not age or not acc_no or not pin or not acc_type:
                    raise ValueError("All fields are required")
                
                if not age.isdigit() or int(age) < 18:
                    raise ValueError("You must be at least 18 years old")
                
                if not re.match(r'^\d{4}$', pin):
                    raise ValueError("PIN must be 4 digits")
                
                if pin != confirm_pin:
                    raise ValueError("PINs do not match")
                
                if acc_type not in ['savings', 'current']:
                    raise ValueError("Account type must be 'savings' or 'current'")
                
                if acc_no in accounts:
                    raise ValueError("Account number already exists")
                
                accounts[acc_no] = BankAccount(name, acc_no, pin, acc_type)
                save_accounts(accounts)
                messagebox.showinfo("Success", f"Thank you {name}, your account has been created!")
                top.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Create Account",
            command=save_account,
            style='Success.TButton'
        ).grid(row=len(fields), column=1, pady=10)
    
    def login_gui(self):
        global current_user
        top = Toplevel(self.root)
        top.title("Login")
        top.geometry("350x200")
        top.resizable(False, False)
        
        ttk.Label(top, text="Account Number:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        acc_entry = ttk.Entry(top)
        acc_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(top, text="PIN:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        pin_entry = ttk.Entry(top, show='*')
        pin_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def verify_login():
            global current_user
            try:
                acc_no = acc_entry.get().strip()
                pin = pin_entry.get().strip()
                
                if acc_no == "admin" and pin == ADMIN_PIN:
                    current_user = None
                    self.admin_tools_gui()
                    top.destroy()
                    return
                
                user = accounts.get(acc_no)
                if not user:
                    raise ValueError("Account not found")
                
                if user.pin != pin:
                    raise ValueError("Invalid PIN")
                
                current_user = user
                self.update_welcome_message()
                self.show_output(f"Login successful!\n\n{user.get_summary()}")
                top.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Login",
            command=verify_login,
            style='Primary.TButton'
        ).grid(row=2, column=1, pady=10)
    
    def logout(self):
        global current_user
        current_user = None
        self.update_welcome_message()
        self.show_output("You have been logged out successfully.")
    
    # Transaction Functions
    def deposit_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        top = Toplevel(self.root)
        top.title("Deposit Money")
        top.geometry("400x200")
        top.resizable(False, False)
        
        ttk.Label(top, text="Amount to Deposit:").pack(pady=(10, 0))
        amount_entry = ttk.Entry(top)
        amount_entry.pack(pady=5)
        
        ttk.Label(top, text="Description (optional):").pack(pady=(10, 0))
        desc_entry = ttk.Entry(top)
        desc_entry.pack(pady=5)
        
        def perform_deposit():
            try:
                amount = float(amount_entry.get())
                description = desc_entry.get().strip()
                
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                current_user.deposit(amount, description)
                save_accounts(accounts)
                
                self.show_output(
                    f"Deposit successful!\n"
                    f"Amount: ₹{amount:.2f}\n"
                    f"New Balance: ₹{current_user.balance:.2f}\n\n"
                    f"{current_user.get_summary()}"
                )
                top.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Deposit",
            command=perform_deposit,
            style='Success.TButton'
        ).pack(pady=10)
    
    def withdraw_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        top = Toplevel(self.root)
        top.title("Withdraw Money")
        top.geometry("400x200")
        top.resizable(False, False)
        
        ttk.Label(top, text="Amount to Withdraw:").pack(pady=(10, 0))
        amount_entry = ttk.Entry(top)
        amount_entry.pack(pady=5)
        
        ttk.Label(top, text="Description (optional):").pack(pady=(10, 0))
        desc_entry = ttk.Entry(top)
        desc_entry.pack(pady=5)
        
        def perform_withdraw():
            try:
                amount = float(amount_entry.get())
                description = desc_entry.get().strip()
                
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                current_user.withdraw(amount, description)
                save_accounts(accounts)
                
                self.show_output(
                    f"Withdrawal successful!\n"
                    f"Amount: ₹{amount:.2f}\n"
                    f"New Balance: ₹{current_user.balance:.2f}\n\n"
                    f"{current_user.get_summary()}"
                )
                top.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Withdraw",
            command=perform_withdraw,
            style='Danger.TButton'
        ).pack(pady=10)
    
    def transfer_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        top = Toplevel(self.root)
        top.title("Transfer Money")
        top.geometry("400x300")
        top.resizable(False, False)
        
        ttk.Label(top, text="Recipient Account Number:").pack(pady=(10, 0))
        recipient_entry = ttk.Entry(top)
        recipient_entry.pack(pady=5)
        
        ttk.Label(top, text="Amount to Transfer:").pack(pady=(10, 0))
        amount_entry = ttk.Entry(top)
        amount_entry.pack(pady=5)
        
        ttk.Label(top, text="Description (optional):").pack(pady=(10, 0))
        desc_entry = ttk.Entry(top)
        desc_entry.pack(pady=5)
        
        def perform_transfer():
            try:
                recipient = recipient_entry.get().strip()
                amount = float(amount_entry.get())
                description = desc_entry.get().strip()
                
                if not recipient:
                    raise ValueError("Recipient account number is required")
                
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                
                if recipient == current_user.account_number:
                    raise ValueError("Cannot transfer to your own account")
                
                target_account = accounts.get(recipient)
                if not target_account:
                    raise ValueError("Recipient account not found")
                
                current_user.transfer(target_account, amount, description)
                save_accounts(accounts)
                
                self.show_output(
                    f"Transfer successful!\n"
                    f"Amount: ₹{amount:.2f}\n"
                    f"To: {target_account.name} ({target_account.account_number})\n"
                    f"New Balance: ₹{current_user.balance:.2f}\n\n"
                    f"{current_user.get_summary()}"
                )
                top.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Transfer",
            command=perform_transfer,
            style='Warning.TButton'
        ).pack(pady=10)
    
    def interest_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        if current_user.account_type.lower() != "savings":
            messagebox.showerror("Error", "Interest only applies to savings accounts")
            return
            
        try:
            interest = current_user.apply_interest()
            save_accounts(accounts)
            
            self.show_output(
                f"Interest applied successfully!\n"
                f"Interest Amount: ₹{interest:.2f}\n"
                f"New Balance: ₹{current_user.balance:.2f}\n\n"
                f"{current_user.get_summary()}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def summary_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        self.show_output(current_user.get_summary())
    
    def transactions_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        top = Toplevel(self.root)
        top.title("Transaction History")
        top.geometry("600x500")
        
        filter_frame = ttk.Frame(top)
        filter_frame.pack(pady=10, fill=X)
        
        ttk.Label(filter_frame, text="Filter by:").pack(side=LEFT, padx=5)
        
        filter_var = StringVar(value="all")
        ttk.Radiobutton(
            filter_frame,
            text="All",
            variable=filter_var,
            value="all"
        ).pack(side=LEFT, padx=5)
        
        ttk.Radiobutton(
            filter_frame,
            text="Deposits",
            variable=filter_var,
            value="deposit"
        ).pack(side=LEFT, padx=5)
        
        ttk.Radiobutton(
            filter_frame,
            text="Withdrawals",
            variable=filter_var,
            value="withdraw"
        ).pack(side=LEFT, padx=5)
        
        ttk.Radiobutton(
            filter_frame,
            text="Transfers",
            variable=filter_var,
            value="transfer"
        ).pack(side=LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Limit:").pack(side=LEFT, padx=5)
        limit_var = StringVar(value="20")
        ttk.OptionMenu(
            filter_frame,
            limit_var,
            "20",
            "10", "20", "50", "100", "All"
        ).pack(side=LEFT, padx=5)
        
        def update_transactions():
            try:
                txn_type = None if filter_var.get() == "all" else filter_var.get()
                limit = None if limit_var.get() == "All" else int(limit_var.get())
                
                transactions = current_user.get_transactions(limit, txn_type)
                
                text_area.config(state=NORMAL)
                text_area.delete(1.0, END)
                
                if not transactions:
                    text_area.insert(END, "No transactions found")
                    return
                
                text_area.insert(END, f"Transaction History ({len(transactions)} records)\n\n")
                for txn in transactions:
                    text_area.insert(END, f"{txn.date} - {txn.txn_type.upper()} ₹{txn.amount:.2f}")
                    if txn.description:
                        text_area.insert(END, f" - {txn.description}")
                    text_area.insert(END, "\n")
                
                text_area.config(state=DISABLED)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        update_btn = ttk.Button(
            filter_frame,
            text="Update",
            command=update_transactions,
            style='Primary.TButton'
        )
        update_btn.pack(side=RIGHT, padx=5)
        
        text_frame = ttk.Frame(top)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        text_area = Text(
            text_frame,
            wrap=WORD,
            font=('Consolas', 10)
        )
        scrollbar = ttk.Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        update_transactions()
    
    def change_pin_gui(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        top = Toplevel(self.root)
        top.title("Change PIN")
        top.geometry("350x200")
        top.resizable(False, False)
        
        ttk.Label(top, text="Current PIN:").pack(pady=(10, 0))
        current_pin_entry = ttk.Entry(top, show='*')
        current_pin_entry.pack(pady=5)
        
        ttk.Label(top, text="New PIN (4-digit):").pack(pady=(10, 0))
        new_pin_entry = ttk.Entry(top, show='*')
        new_pin_entry.pack(pady=5)
        
        ttk.Label(top, text="Confirm New PIN:").pack(pady=(10, 0))
        confirm_pin_entry = ttk.Entry(top, show='*')
        confirm_pin_entry.pack(pady=5)
        
        def perform_pin_change():
            try:
                current_pin = current_pin_entry.get()
                new_pin = new_pin_entry.get()
                confirm_pin = confirm_pin_entry.get()
                
                if current_user.pin != current_pin:
                    raise ValueError("Current PIN is incorrect")
                
                if new_pin != confirm_pin:
                    raise ValueError("New PINs do not match")
                
                current_user.change_pin(new_pin)
                save_accounts(accounts)
                
                messagebox.showinfo("Success", "PIN changed successfully!")
                top.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(
            top,
            text="Change PIN",
            command=perform_pin_change,
            style='Primary.TButton'
        ).pack(pady=10)
    
    def show_balance_history(self):
        if not current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        if not current_user.transactions:
            messagebox.showinfo("Info", "No transaction history available")
            return
            
        history = current_user.get_balance_history()
        if not history:
            return
            
        top = Toplevel(self.root)
        top.title("Balance History")
        top.geometry("600x500")
        
        text_frame = ttk.Frame(top)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        text_area = Text(
            text_frame,
            wrap=WORD,
            font=('Consolas', 10)
        )
        scrollbar = ttk.Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        text_area.config(state=NORMAL)
        text_area.delete(1.0, END)
        
        text_area.insert(END, f"Balance History for Account {current_user.account_number}\n")
        text_area.insert(END, f"Current Balance: ₹{current_user.balance:.2f}\n\n")
        
        text_area.insert(END, "Date/Time                Balance\n")
        text_area.insert(END, "--------------------------------\n")
        
        for date, balance in history:
            text_area.insert(END, f"{date}  ₹{balance:.2f}\n")
        
        text_area.config(state=DISABLED)
        
        ttk.Button(
            top,
            text="Close",
            command=top.destroy,
            style='Danger.TButton'
        ).pack(pady=10)
    
    # Admin Functions
    def admin_tools_gui(self):
        top = Toplevel(self.root)
        top.title("Admin Tools")
        top.geometry("600x500")
        
        ttk.Label(
            top,
            text="Admin Tools - Account Management",
            style='Header.TLabel'
        ).pack(pady=10)
        
        # Search Frame
        search_frame = ttk.Frame(top)
        search_frame.pack(pady=10, fill=X)
        
        ttk.Label(search_frame, text="Search Account:").pack(side=LEFT, padx=5)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=LEFT, padx=5, expand=True, fill=X)
        
        def search_account():
            search_term = search_entry.get().strip()
            if not search_term:
                return
                
            results = []
            for acc_no, account in accounts.items():
                if (search_term in acc_no or 
                    search_term.lower() in account.name.lower()):
                    results.append(account)
            
            text_area.config(state=NORMAL)
            text_area.delete(1.0, END)
            
            if not results:
                text_area.insert(END, "No accounts found")
                return
                
            text_area.insert(END, f"Found {len(results)} accounts:\n\n")
            for account in results:
                text_area.insert(END, f"Account: {account.account_number}\n")
                text_area.insert(END, f"Name: {account.name}\n")
                text_area.insert(END, f"Type: {account.account_type}\n")
                text_area.insert(END, f"Balance: ₹{account.balance:.2f}\n")
                text_area.insert(END, f"Created: {account.creation_date}\n")
                text_area.insert(END, f"Last Access: {account.last_accessed}\n")
                text_area.insert(END, "-"*50 + "\n")
            
            text_area.config(state=DISABLED)
        
        ttk.Button(
            search_frame,
            text="Search",
            command=search_account,
            style='Primary.TButton'
        ).pack(side=LEFT, padx=5)
        
        # Stats Frame
        stats_frame = ttk.Frame(top)
        stats_frame.pack(pady=10, fill=X)
        
        def show_stats():
            total_accounts = len(accounts)
            savings = sum(1 for acc in accounts.values() if acc.account_type.lower() == "savings")
            current = total_accounts - savings
            total_balance = sum(acc.balance for acc in accounts.values())
            
            text_area.config(state=NORMAL)
            text_area.delete(1.0, END)
            text_area.insert(END, "Bank Statistics:\n\n")
            text_area.insert(END, f"Total Accounts: {total_accounts}\n")
            text_area.insert(END, f"Savings Accounts: {savings}\n")
            text_area.insert(END, f"Current Accounts: {current}\n")
            text_area.insert(END, f"Total Bank Balance: ₹{total_balance:.2f}\n")
            text_area.config(state=DISABLED)
        
        ttk.Button(
            stats_frame,
            text="Show Statistics",
            command=show_stats,
            style='Success.TButton'
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            stats_frame,
            text="List All Accounts",
            command=lambda: self.list_all_accounts(text_area),
            style='Primary.TButton'
        ).pack(side=LEFT, padx=5)
        
        # Text Area
        text_frame = ttk.Frame(top)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        text_area = Text(
            text_frame,
            wrap=WORD,
            font=('Consolas', 10)
        )
        scrollbar = ttk.Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        show_stats()
    
    def list_all_accounts(self, text_area):
        text_area.config(state=NORMAL)
        text_area.delete(1.0, END)
        
        if not accounts:
            text_area.insert(END, "No accounts in the system")
            return
            
        text_area.insert(END, "All Accounts:\n\n")
        for acc_no, account in accounts.items():
            text_area.insert(END, f"Account: {acc_no}\n")
            text_area.insert(END, f"Name: {account.name}\n")
            text_area.insert(END, f"Type: {account.account_type}\n")
            text_area.insert(END, f"Balance: ₹{account.balance:.2f}\n")
            text_area.insert(END, f"Created: {account.creation_date}\n")
            text_area.insert(END, f"Last Access: {account.last_accessed}\n")
            text_area.insert(END, "-"*50 + "\n")
        
        text_area.config(state=DISABLED)

# Initialize and run the application
if __name__ == "__main__":
    root = Tk()
    app = SmartBankApp(root)
    root.mainloop()