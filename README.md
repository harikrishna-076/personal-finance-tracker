# Personal Finance Tracker & Budget Planner (CSV Edition)

An interactive, Object-Oriented command-line finance tracking tool. This application uses a local CSV-based database for zero-setup data persistence, and leverages Pandas and Matplotlib for analytics and trends.

This project is optimized to showcase core skills for entry-level Software Engineer and Data Analyst roles.

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

## Resume Highlights (ATS-Optimized)

*   **Software Engineering & OOP**: Standard Python class designs, encapsulation, parameter validation, and separation of concerns.
*   **Data Persistence (CSV)**: Managing structured data tables in flat CSV files, generating row index mappings, and updating/deleting records programmatically.
*   **Data Aggregation & Filtering (Pandas)**: Loading datasets into DataFrames, filtering records by custom datetime ranges, utilizing `groupby` sums, and merging tables for budget checks.
*   **Data Visualization (Matplotlib)**: Customizing trend line configurations, labels, gridlines, color formatting (Green for Income, Red for Expense), and exporting plots to image files.

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
