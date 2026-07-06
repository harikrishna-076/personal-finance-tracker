import sys
from datetime import datetime
from csv_manager import CSVManager
from models import Transaction, Budget
from analysis import FinanceAnalyzer

def display_menu():
    print("\n" + "=" * 45)
    print("   PERSONAL FINANCE & BUDGET DASHBOARD")
    print("=" * 45)
    print("1. Record Transaction (Income / Expense)")
    print("2. Set Category Monthly Budget Limit")
    print("3. View Transaction Ledger")
    print("4. View Transactions & Summary within Date Range")
    print("5. View Budget Dashboard")
    print("6. View Net Monthly Savings Trend(graph)")
    print("7. Delete a Transaction")
    print("0. Exit Application")
    print("=" * 45)

def get_valid_amount(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                print("Amount must be positive. Try again.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        if date_str == "":
            return ""
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("Invalid format. Please use DD-MM-YYYY (e.g., 01-04-2026) or press Enter for today.")

def get_valid_month(prompt):
    while True:
        month_str = input(prompt).strip()
        if month_str == "":
            return datetime.today().strftime("%m-%Y")
        try:
            datetime.strptime(month_str, "%m-%Y")
            return month_str
        except ValueError:
            print("Invalid format. Please enter as MM-YYYY (e.g., 04-2026).")

def main():
    try:
        db = CSVManager()
    except Exception:
        print("Could not initialize storage. Exiting.")
        sys.exit(1)
        
    analyzer = FinanceAnalyzer(db)

    while True:
        display_menu()
        choice = input("Select an option (0-7): ").strip()

        if choice == "1":
            print("\n--- Record New Transaction ---")
            
            while True:
                cat_input = input("Select type (i for Income, e for Expense): ").strip().lower()
                if cat_input.lower() == 'i':
                    category = "Income"
                    break
                elif cat_input.lower() == 'e':
                    category = "Expense"
                    break
                else:
                    print("Invalid option. Please enter 'i' or 'e'.")
            
            amount = get_valid_amount("Enter Amount ($): ")
            date = get_valid_date("Enter Date (DD-MM-YYYY, leave empty for today): ")
            description = input("Enter Description (e.g. salary, grocery, transport): ").strip()
            if not description:
                description = "Uncategorized"

            try:
                new_t = Transaction(date, amount, category, description)
                success = db.add_transaction(new_t)
                if success:
                    print(f"Transaction recorded: {new_t}")
                else:
                    print("Could not save to file.")
            except ValueError as e:
                print(f"Validation Error: {e}")

        elif choice == "2":
            print("\n--- Set Category Monthly Budget Limit ---")
            item = input("Enter Item Name (e.g. grocery, transport): ").strip()
            if not item:
                print("Item cannot be empty!")
                continue
            limit = get_valid_amount("Enter Monthly Budget Limit $: ")
            month = get_valid_month("Enter Month (MM-YYYY, leave empty for current month): ")

            try:
                new_b = Budget(item, limit, month)
                success = db.add_budget(new_b)
                if success:
                    print(f"Budget configured successfully: {new_b}")
                else:
                    print("Could not save budget limit.")
            except ValueError as e:
                print(f"Validation Error: {e}")

        elif choice == "3":
            print("\n--- Transaction Ledger ---")
            records = db.get_all_transactions()
            if not records:
                print("No transactions found.")
            else:
                print(f"{'Index':<6} | {'Date':<10} | {'Category':<8} | {'Amount':<10} | {'Description'}")
                print("-" * 65)
                for idx, r in enumerate(records, 1):
                    print(f"[{idx:<3}] | {r}")
                
                total_income = sum(r.amount for r in records if r.category == "Income")
                total_expenses = sum(r.amount for r in records if r.category == "Expense")
                net_worth = total_income - total_expenses
                
                print("-" * 65)
                print(f"Total Income:   ${total_income:.2f}")
                print(f"Total Expenses: ${total_expenses:.2f}")
                print(f"Net Worth:      ${net_worth:.2f}")
                print("-" * 65)

        elif choice == "4":
            print("\n--- View Transactions & Summary within Date Range ---")
            start = get_valid_date("Enter Start Date (DD-MM-YYYY): ")
            if not start:
                print("Start Date is required.")
                continue
            end = get_valid_date("Enter End Date (DD-MM-YYYY): ")
            if not end:
                print("End Date is required.")
                continue

            filtered_df, inc, exp, net = analyzer.get_summary_within_range(start, end)
            if filtered_df.empty:
                print(f"No transactions found between {start} and {end}.")
            else:
                print(f"\n--- Records between {start} and {end} ---")
                print(f"{'Index':<6} | {'Date':<10} | {'Category':<8} | {'Amount':<10} | {'Description'}")
                print("-" * 65)
                for index, row in filtered_df.iterrows():
                    sign = "+" if row["category"] == "Income" else "-"
                    amount_str = f"{sign}${row['amount']:.2f}"
                    print(f"[{index + 1:<3}] | {row['date']:<10} | {row['category']:<8} | {amount_str:<10} | {row['description']}")
                print("-" * 65)
                print(f"Total Income:   ${inc:.2f}")
                print(f"Total Expenses: ${exp:.2f}")
                print(f"Net Worth:      ${net:.2f}")
                print("-" * 65)

        elif choice == "5":
            print("\n--- Budget Dashboard ---")
            warnings = analyzer.check_budgets()
            if warnings.empty:
                print("No budgets set or no transaction matches found.")
            else:
                print(f"{'Item (Category)':<15} | {'Month':<8} | {'Spent':<10} | {'Limit':<10} | {'Status':<15}")
                print("-" * 65)
                for index, row in warnings.iterrows():
                    status = "OK"
                    if row["difference"] > 0:
                        status = f"EXCEEDED by ${row['difference']:.2f}"
                    elif row["difference"] == 0:
                        status = "LIMIT REACHED"
                    else:
                        status = f"Remaining: ${abs(row['difference']):.2f}"
                        
                    print(f"{row['item']:<15} | {row['month']:<8} | ${row['actual']:<9.2f} | ${row['limit_amount']:<9.2f} | {status}")

        elif choice == "6":
            print("\n--- Net Monthly Savings Trend Line Plot ---")
            analyzer.plot_monthly_savings_trend()

        elif choice == "7":
            print("\n--- Delete Transaction ---")
            records = db.get_all_transactions()
            if not records:
                print("No transactions found to delete.")
                continue
                
            print(f"{'Index':<6} | {'Date':<10} | {'Category':<8} | {'Amount':<10} | {'Description'}")
            print("-" * 65)
            for idx, r in enumerate(records, 1):
                print(f"[{idx:<3}] | {r}")
                
            try:
                t_idx = int(input("\nEnter the line number [] to delete: "))
                confirm = input(f"Are you sure you want to delete line {t_idx}? (y/n): ").strip().lower()
                if confirm == "y":
                    deleted = db.delete_transaction_by_index(t_idx)
                    if deleted:
                        print(f"Transaction line {t_idx} deleted successfully.")
                    else:
                        print(f"Invalid index {t_idx}.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid input. Please enter a valid line number.")

        elif choice == "0":
            print("\nClosing dashboard...")
            break
        else:
            print("Invalid menu selection. Please choose an option between 0 and 7.")

if __name__ == "__main__":
    main()
