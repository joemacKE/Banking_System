from dataclasses import dataclass
from datetime import datetime

@dataclass
class CustomerData:
    full_name: str
    customer_ID: int
    base_salary: float
    balance: float

@dataclass
class Transaction:
    amount: float
    type: str  # e.g., deposit, withdrawal, overdraft, interest
    description: str
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class BankAccount:
    def __init__(self, customer_data: CustomerData):
        self._id = customer_data.customer_ID
        self._name = customer_data.full_name
        self._base_salary = customer_data.base_salary
        self._balance = customer_data.balance
        self._transactions = []

    def log_transaction(self, amount, type, description):
        self._transactions.append(Transaction(
            amount=amount,
            type=type,
            description=description,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    def deposit(self, amount):
        if amount >= 100:
            self._balance += amount
            self.log_transaction(amount, "deposit", "Deposited funds")
            print(f"Deposited {amount} to your account.")
        else:
            print("Minimum deposit should be 100.")

    def withdraw(self, amount):
        if amount >= 100 and amount <= self._balance:
            self._balance -= amount
            self.log_transaction(amount, "withdrawal", "Withdrew funds")
            print(f"Withdrew {amount} successfully.")
        else:
            print("Insufficient balance or invalid amount.")

    def get_account_summary(self):
        print("\n--- Account Summary ---")
        print(f"Customer ID: {self._id}")
        print(f"Name: {self._name}")
        print(f"Current Balance: {self._balance}")
        print(f"Total Transactions: {len(self._transactions)}")

    def get_transaction_history(self):
        print("\n--- Transaction History ---")
        if not self._transactions:
            print("No transactions recorded.")
        else:
            for txn in self._transactions:
                print(f"{txn.timestamp} | {txn.type.title()} | Amount: {txn.amount} | {txn.description}")

class SavingsAccount(BankAccount):
    def __init__(self, customer_data: CustomerData, overdraft=1000):
        super().__init__(customer_data)
        self.overdraft_limit = overdraft

    def use_overdraft(self, amount):
        if self._balance < amount <= self.overdraft_limit:
            self._balance -= amount
            self.log_transaction(amount, "overdraft", "Overdraft applied")
            print(f"Overdraft of {amount} applied. New balance: {self._balance}")
        else:
            print("Overdraft limit exceeded or invalid request.")

class FixedDeposit(BankAccount):
    def __init__(self, customer_data: CustomerData, locked_in=12, interest_rate=0.05):
        super().__init__(customer_data)
        self.locked_in = locked_in
        self.interest_rate = interest_rate

    def withdrawal_before_maturity(self, amount):
        if self.locked_in <= 0:
            self.withdraw(amount)
        else:
            print(f"Withdrawal not allowed. Maturity in {self.locked_in} months.")

    def maturity_amount(self):
        try:
            total = self._balance * self.interest_rate * self.locked_in
            self.log_transaction(total, "interest", "Interest accrued at maturity")
            print(f"Maturity amount: {total}")
            return total
        except Exception as e:
            print(f"Error calculating maturity amount: {e}")
            return 0

class BankSystem:
    def __init__(self):
        self.account = []

    def add_account(self, account):
        try:
            self.account.append(account)
            print("Account added.")
        except Exception as e:
            print(f"Error adding account: {e}")

    def remove_account(self, account):
        try:
            self.account.remove(account)
            print("Account removed.")
        except Exception as e:
            print(f"Error removing account: {e}")

    def show_all_accounts(self):
        for acc in self.account:
            acc.get_account_summary()
