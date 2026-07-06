import os
import csv
from models import Transaction, Budget

class CSVManager:
    def __init__(self):
        self.transactions_file = "transactions.csv"
        self.budgets_file = "budgets.csv"
        self.init_files()

    def init_files(self):
        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["date", "amount", "category", "description"])
                
        if not os.path.exists(self.budgets_file):
            with open(self.budgets_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["item", "limit_amount", "month"])

    def add_transaction(self, t):
        with open(self.transactions_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([t.date, t.amount, t.category, t.description])
        return True

    def get_all_transactions(self):
        transactions = []
        if not os.path.exists(self.transactions_file):
            return transactions
            
        with open(self.transactions_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = Transaction(
                    date=row["date"],
                    amount=float(row["amount"]),
                    category=row["category"],
                    description=row["description"]
                )
                transactions.append(t)
        return transactions

    def add_budget(self, b):
        budgets = self.get_all_budgets()
        
        updated = False
        for i, existing in enumerate(budgets):
            if existing.item == b.item and existing.month == b.month:
                budgets[i] = b
                updated = True
                break
                
        if not updated:
            budgets.append(b)
            
        with open(self.budgets_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["item", "limit_amount", "month"])
            for existing in budgets:
                writer.writerow([existing.item, existing.limit_amount, existing.month])
        return True

    def get_all_budgets(self):
        budgets = []
        if not os.path.exists(self.budgets_file):
            return budgets
            
        with open(self.budgets_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                b = Budget(
                    item=row["item"],
                    limit_amount=float(row["limit_amount"]),
                    month=row["month"]
                )
                budgets.append(b)
        return budgets

    def delete_transaction_by_index(self, index_1_based):
        transactions = self.get_all_transactions()
        index = index_1_based - 1
        
        if index < 0 or index >= len(transactions):
            return False
            
        transactions.pop(index)
        
        with open(self.transactions_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "description"])
            for t in transactions:
                writer.writerow([t.date, t.amount, t.category, t.description])
        return True
