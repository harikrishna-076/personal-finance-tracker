from datetime import datetime

class Transaction:
    def __init__(self, date, amount, category, description):
        self.category = category.strip()
        if self.category not in ["Income", "Expense"]:
            raise ValueError("Category must be 'Income' or 'Expense'.")
            
        if float(amount) <= 0:
            raise ValueError("Amount must be a positive number.")
        self.amount = float(amount)
        
        if date is None or date.strip() == "":
            self.date = datetime.today().strftime("%d-%m-%Y")
        else:
            try:
                datetime.strptime(date.strip(), "%d-%m-%Y")
                self.date = date.strip()
            except ValueError:
                raise ValueError("Date must be in DD-MM-YYYY format.")
                
        self.description = description.strip()

    def __str__(self):
        sign = "+" if self.category == "Income" else "-"
        amount_str = f"{sign}${self.amount:.2f}"
        return f"{self.date:<10} | {self.category:<8} | {amount_str:<10} | {self.description}"


class Budget:
    def __init__(self, item, limit_amount, month):
        self.item = item.strip()
        
        if float(limit_amount) <= 0:
            raise ValueError("Budget limit must be a positive number.")
        self.limit_amount = float(limit_amount)
        
        try:
            datetime.strptime(month.strip(), "%m-%Y")
            self.month = month.strip()
        except ValueError:
            raise ValueError("Month must be in MM-YYYY format.")

    def __str__(self):
        return f"[{self.month}] Item: {self.item} | Limit: ${self.limit_amount:.2f}"
