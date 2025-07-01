from dataclasses import dataclass
@dataclass
class CustomerData:
    full_name: str
    customer_ID: int
    base_salary: float
    balance: float

class BankAccount:
    def __init__(self, customer_data:CustomerData):
        self._id = customer_data.customer_ID
        self._name = customer_data.full_name
        self._base_salary = customer_data.base_salary
        self._balance = customer_data.balance


    

    def deposit(self, amount):
        try:
            if amount >= 100:
                self._balance += amount
                print(f"Deposited {amount} to you account")
                
            else:
                print("Minimum deposit should be 100")
                
        except ValueError as e:
            print("Invalid amount")
    
    def withdraw(self, amount):
        try:
            if amount <= self._balance and amount >= 100:
                self._balance -= amount
                print(f"Withdrew {amount} succesfully")
            else:
                print("You have insufficient balance")
        except Exception as e:
            print(f"Withdrawal fail")

    def get_account_summary(self):
        print("\n --- Account --_")
        print(f"Customer ID: {self._id}")
        print(f"Name: {self._name}")
        print(f"Current Balance: {self._balance}")
        print(f"{self.deposit()}")
        print(f"{self.withdraw()}")



class SavingsAccount(BankAccount):
    def __init__(self, customer_data:CustomerData):
        super().__init__(customer_data)

    
    def user_overdraft(self, amount):
        try:
            if self._balance < amount <= amount:
                self._balance -= amount
                print(f"Overdraft of amount {amount} is applied to your account")
            else:
                print(f"The minimum overdraft withdrawal is {amount}")
        except Exception as e:
            print(f"{e}")


class FixedDeposit(BankAccount):
    def __init__(self, customer_data:CustomerData, locked_in = 12, interest_rate = 0.5):
        super().__init__(customer_data)
        self.locked_in = locked_in
        self.interest_rate = interest_rate
    
    def withdrawal_before_maturity(self, amount):
        try:
            if self.locked_in <= 0:
                self.withdraw(amount)
            else:
                print(f"Cannot withdraw. Maturity is due in {self.locked_in} months")
        
        except Exception as e:
            print(f"{e}")
        

    def maturity_amount(self):
        try:
            total = self._balance * self.interest_rate * self.locked_in
            print(f"Maturity amount will be: {total}")
            return total
        except Exception as e:
            print(f"Sorry something went wrong: {e}")
    

class BankSystem:
    def __init__(self):
        self.account = []

    def add_account(self, account):
        try:
            self.account.append(account)
        except Exception as e:
            print(f"Error adding account: {e}")
    
    def remove_account(self, account):
        try:
            self.account.remove(account)
            print(f"Account removed succesfully")
        except Exception as e:
            print(f"Something went wrong! Failed to remove account")
    

import unittest
from banking_system import CustomerData, BankAccount, SavingsAccount, FixedDeposit, BankSystem  # Assuming saved as banking.py

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.data = CustomerData("John Doe", 1001, 50000, 1000)
        self.savings = SavingsAccount(self.data, overdraft=2000)
        self.fixed = FixedDeposit(self.data, locked_in=6, interest_rate=0.1)

    def test_deposit_valid(self):
        self.savings.deposit(500)
        self.assertEqual(self.savings._balance, 1500)

    def test_deposit_invalid(self):
        self.savings.deposit(-200)
        self.assertEqual(self.savings._balance, 1000)  # No change

    def test_withdraw_valid(self):
        self.savings.withdraw(500)
        self.assertEqual(self.savings._balance, 500)

    def test_withdraw_invalid(self):
        self.savings.withdraw(1500)
        self.assertEqual(self.savings._balance, 1000)  # No change

    def test_overdraft_valid(self):
        self.savings.use_overdraft(1500)
        self.assertEqual(self.savings._balance, -500)

    def test_fixed_maturity_amount(self):
        total = self.fixed.maturity_amount()
        expected = 1000 * 0.1 * 6
        self.assertEqual(total, expected)

    def test_add_account_to_system(self):
        bank = BankSystem()
        bank.add_account(self.savings)
        self.assertIn(self.savings, bank.account)

    def test_remove_account_from_system(self):
        bank = BankSystem()
        bank.add_account(self.savings)
        bank.remove_account(self.savings)
        self.assertNotIn(self.savings, bank.account)

if __name__ == '__main__':
    unittest.main()
