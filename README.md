# Personal Finance Tracker & Budget Planner (CSV Edition)

An interactive, Object-Oriented command-line finance tracking tool. This application uses a local CSV-based database for zero-setup data persistence, and leverages Pandas and Matplotlib for analytics and trends.

---

## Key Features

*   **Interactive OOP Dashboard**: A clean command-line interface to record transactions (incomes and expenses), set monthly budgets, and track balances.
*   **Simple Input Selection**: Quick shortcuts to select transaction types (`i` for Income and `e` for Expense).
*   **Custom CSV Database Persistence**: Reads and writes records directly to `transactions.csv` and `budgets.csv` using the custom schema format:
    *   `transactions.csv`: `date,amount,category,description`
    *   `budgets.csv`: `item,limit_amount,month`
*   **Date-Range Filtering**: Search and display transactions within a specific date range (DD-MM-YYYY format) and calculate range summary metrics (Total Income, Total Expenses, Net Savings).
*   **Budget Compliance Dashboard**: Compares item budgets (e.g. grocery, rent) against actual expenditures in a month.
*   **Savings Trend Graph**: Generates a custom line trend chart using Matplotlib to visualize monthly total income (green line) vs. expenses (red line) over time.

---

## What is the Use of This Project?

The Personal Finance Tracker & Budget Planner is designed to help individuals take control of their financial health. It provides a simple, clean, and zero-setup command-line interface to log daily transactions (income and expenses) and establish monthly category budget limits.

## How is It Useful?

*   **Prevent Overspending**: Set specific budgets for categories (like grocery, entertainment, transport) and instantly check your budget compliance dashboard to see remaining funds or flags when limits are exceeded.
*   **Visual Financial Trends**: Rather than analyzing raw numbers, visualize your monthly cash flow with generated line trend charts that highlight total monthly income versus total monthly expenses.
*   **Date-Specific Reporting**: Search and aggregate logs within custom date ranges to analyze spending habits during holidays, trips, or specific months.
*   **Zero-Setup Portability**: Uses a simple local CSV file database, meaning no external servers, database installations, or cloud services are required. Your data stays private and localized.

---

## Project Structure

```
personal_finance_tracker/
├── models.py             # OOP Models (Transaction and Budget classes)
├── csv_manager.py        # CSV database file manager (saves, reads, and deletes data)
├── analysis.py           # Data processing and Matplotlib line trend plotting
├── main.py               # Main CLI interface and dashboard loop
├── requirements.txt      # Project library dependencies
└── README.md             # Project documentation (this file)
```

---

## Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/personal-finance-tracker.git
    cd personal-finance-tracker
    ```

2.  **Install Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    python main.py
    ```
