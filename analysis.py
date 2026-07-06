import os
import pandas as pd
import matplotlib.pyplot as plt
from csv_manager import CSVManager

class FinanceAnalyzer:
    def __init__(self, csv_manager: CSVManager):
        self.csv_mgr = csv_manager

    def load_transactions_df(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_mgr.transactions_file):
            return pd.DataFrame(columns=["date", "amount", "category", "description"])
        
        try:
            df = pd.read_csv(self.csv_mgr.transactions_file)
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
                df["amount"] = pd.to_numeric(df["amount"])
            return df
        except Exception:
            return pd.DataFrame(columns=["date", "amount", "category", "description"])

    def load_budgets_df(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_mgr.budgets_file):
            return pd.DataFrame(columns=["item", "limit_amount", "month"])
            
        try:
            df = pd.read_csv(self.csv_mgr.budgets_file)
            if not df.empty:
                df["limit_amount"] = pd.to_numeric(df["limit_amount"])
            return df
        except Exception:
            return pd.DataFrame(columns=["item", "limit_amount", "month"])

    def check_budgets(self) -> pd.DataFrame:
        transactions_df = self.load_transactions_df()
        budgets_df = self.load_budgets_df()

        if transactions_df.empty or budgets_df.empty:
            return pd.DataFrame(columns=["item", "month", "actual", "limit_amount", "difference"])

        expenses_df = transactions_df[transactions_df["category"] == "Expense"].copy()
        if expenses_df.empty:
            return pd.DataFrame(columns=["item", "month", "actual", "limit_amount", "difference"])
            
        expenses_df["month"] = expenses_df["date"].dt.strftime("%m-%Y")
        
        monthly_expenses = expenses_df.groupby(["description", "month"])["amount"].sum().reset_index()
        monthly_expenses.rename(columns={"amount": "actual", "description": "item"}, inplace=True)

        merged = pd.merge(monthly_expenses, budgets_df, on=["item", "month"], how="inner")
        merged["difference"] = merged["actual"] - merged["limit_amount"]
        return merged

    def get_summary_within_range(self, start_date_str, end_date_str):
        df = self.load_transactions_df()
        if df.empty:
            return pd.DataFrame(), 0.0, 0.0, 0.0

        try:
            start_dt = pd.to_datetime(start_date_str, format="%d-%m-%Y")
            end_dt = pd.to_datetime(end_date_str, format="%d-%m-%Y")
        except ValueError:
            print("Invalid date formats entered.")
            return pd.DataFrame(), 0.0, 0.0, 0.0

        mask = (df["date"] >= start_dt) & (df["date"] <= end_dt)
        filtered_df = df[mask].copy()

        if filtered_df.empty:
            return filtered_df, 0.0, 0.0, 0.0

        total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
        net_savings = total_income - total_expense

        filtered_df = filtered_df.sort_values(by="date")
        filtered_df["date"] = filtered_df["date"].dt.strftime("%d-%m-%Y")

        return filtered_df, float(total_income), float(total_expense), float(net_savings)

    def plot_monthly_savings_trend(self):
        df = self.load_transactions_df()
        if df.empty:
            print("No transaction data available to plot trends.")
            return

        df = df.sort_values(by="date")
        df["month_period"] = df["date"].dt.to_period("M")

        monthly_income = df[df["category"] == "Income"].groupby("month_period")["amount"].sum()
        monthly_expense = df[df["category"] == "Expense"].groupby("month_period")["amount"].sum()

        monthly_summary = pd.DataFrame({"Income": monthly_income, "Expense": monthly_expense}).fillna(0)
        monthly_summary = monthly_summary.sort_index()

        if monthly_summary.empty:
            print("Insufficient monthly transaction data to plot trend.")
            return

        x_labels = [m.strftime("%m-%Y") for m in monthly_summary.index]

        plt.figure(figsize=(10, 5))
        
        plt.plot(
            x_labels, 
            monthly_summary["Income"], 
            marker="o", 
            linewidth=2.5, 
            color="#2ecc71", 
            label="Total Income"
        )
        
        plt.plot(
            x_labels, 
            monthly_summary["Expense"], 
            marker="o", 
            linewidth=2.5, 
            color="#e74c3c", 
            label="Total Expenses"
        )

        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Amount ($)", fontsize=12)
        plt.title("Monthly Income vs. Expenses Trend", fontsize=14, fontweight="bold")
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        filename = "savings_trend.png"
        plt.savefig(filename, dpi=300)
        print(f"Savings trend line chart saved as '{filename}'.")
        plt.show()
