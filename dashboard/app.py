import streamlit as st
import pandas as pd
import os
from pathlib import Path
import plotly.express as px
from datetime import datetime
import csv
import json

# --- File Paths ---
BASE_DIR = Path(__file__).resolve().parents[1]
TRANSACTIONS_FILE = BASE_DIR / "database" / "transactions.txt"
BUDGETS_FILE = BASE_DIR / "database" / "budgets.txt"
EXPORT_DIR = BASE_DIR / "exports"

# --- Constants ---
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]

# --- Data Loading ---
def load_transactions():
    try:
        if not TRANSACTIONS_FILE.exists():
            return pd.DataFrame(columns=["date", "type", "category", "description", "amount"])
        
        rows = []
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    rows.append(parts)
        
        df = pd.DataFrame(rows, columns=["date", "type", "category", "description", "amount"])
        df["amount"] = df["amount"].astype(int)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        st.error(f"Error loading transactions: {e}")
        return pd.DataFrame(columns=["date", "type", "category", "description", "amount"])

def load_budgets():
    try:
        if not BUDGETS_FILE.exists():
            return pd.DataFrame(columns=["category", "limit"])
        
        rows = []
        with open(BUDGETS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    rows.append(parts)
        
        df = pd.DataFrame(rows, columns=["category", "limit"])
        df["limit"] = df["limit"].astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading budgets: {e}")
        return pd.DataFrame(columns=["category", "limit"])

# --- UI Pages ---

def dashboard_page(transactions, budgets):
    st.title("📊 Personal Finance Dashboard")
    st.write("A simple visual overview of your income, expenses, and budgets.")

    if transactions.empty:
        st.info("No transactions found. Add some data first.")
        st.stop()

    total_income = transactions[transactions["type"] == "income"]["amount"].sum()
    total_expense = transactions[transactions["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"PKR {total_income/100:,.2f}")
    col2.metric("Total Expenses", f"PKR {total_expense/100:,.2f}")
    col3.metric("Current Balance", f"PKR {balance/100:,.2f}")

    st.markdown("---")

    st.subheader("💸 Expense Breakdown by Category")
    expenses = transactions[transactions["type"] == "expense"]
    if not expenses.empty:
        pie_data = expenses.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(pie_data, values='amount', names='category', title='Expense Distribution')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No expense data available.")

    st.markdown("---")

    if not budgets.empty:
        st.subheader("📉 Budgets vs Actual Spending")
        merged = expenses.groupby("category")["amount"].sum().reset_index()
        merged = merged.merge(budgets, on="category", how="left").fillna(0)
        merged["amount"] = merged["amount"] / 100
        merged["limit"] = merged["limit"] / 100
        fig2 = px.bar(merged, x='category', y=['amount', 'limit'], barmode='group', title="Budget vs. Spending")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No budgets set.")

def transactions_page(transactions):
    st.title("💸 Transactions")

    st.subheader("Add New Transaction")
    transaction_type = st.selectbox("Type", ["expense", "income"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    category = st.selectbox("Category", EXPENSE_CATEGORIES if transaction_type == "expense" else INCOME_CATEGORIES)
    description = st.text_input("Description")
    date = st.date_input("Date", datetime.now())

    if st.button("Add Transaction"):
        if amount > 0:
            with open(TRANSACTIONS_FILE, "a") as f:
                f.write(f"{date.strftime('%Y-%m-%d')},{transaction_type},{category},{description},{int(amount*100)}\n")
            st.success("Transaction added successfully!")
            st.rerun()
        else:
            st.error("Amount must be positive.")

    st.markdown("---")
    st.subheader("📄 All Transactions")
    
    # Filtering
    all_dates = pd.to_datetime(transactions['date']).dt.date
    min_date, max_date = all_dates.min(), all_dates.max()
    
    date_range = st.date_input("Filter by date range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_transactions = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]
        display_transactions = filtered_transactions.copy()
        display_transactions["amount"] = display_transactions["amount"] / 100
        st.dataframe(display_transactions)

def budgets_page(budgets):
    st.title("💰 Budgets")

    st.subheader("Set New Budget")
    category = st.selectbox("Category", EXPENSE_CATEGORIES)
    limit = st.number_input("Budget Amount", min_value=0.0, step=1.0)

    if st.button("Set Budget"):
        if limit > 0:
            existing_budgets = budgets.set_index('category').to_dict()['limit']
            existing_budgets[category] = int(limit * 100)
            with open(BUDGETS_FILE, "w") as f:
                for cat, lim in existing_budgets.items():
                    f.write(f"{cat},{lim}\n")
            st.success("Budget set successfully!")
            st.rerun()
        else:
            st.error("Budget amount must be positive.")

    st.markdown("---")
    st.subheader("📊 Current Budgets")
    st.dataframe(budgets.assign(limit=lambda df: df["limit"] / 100))

def analytics_page(transactions, budgets):
    st.title("📈 Financial Analytics")

    if transactions.empty:
        st.info("No transactions found for analysis.")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Spending Analysis
    st.subheader("Spending Analysis")
    current_month_expenses = transactions[
        (transactions["date"].dt.month == current_month) & 
        (transactions["date"].dt.year == current_year) & 
        (transactions["type"] == "expense")
    ]
    if not current_month_expenses.empty:
        spending_by_category = current_month_expenses.groupby("category")["amount"].sum()
        st.bar_chart(spending_by_category / 100)
    else:
        st.write("No expenses this month.")

    # Income Analysis
    st.subheader("Income Analysis")
    current_month_income = transactions[
        (transactions["date"].dt.month == current_month) & 
        (transactions["date"].dt.year == current_year) & 
        (transactions["type"] == "income")
    ]
    if not current_month_income.empty:
        income_by_source = current_month_income.groupby("category")["amount"].sum()
        st.bar_chart(income_by_source / 100)
    else:
        st.write("No income this month.")

    # Savings Analysis
    st.subheader("Savings Analysis")
    total_income = current_month_income["amount"].sum()
    total_expenses = current_month_expenses["amount"].sum()
    savings = total_income - total_expenses
    st.metric("Monthly Savings", f"PKR {savings/100:,.2f}")
    
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
    st.metric("Savings Rate", f"{savings_rate:.2f}%")

    # Financial Health Score
    st.subheader("Financial Health Score")
    savings_score = 30 if savings_rate >= 20 else (20 if savings_rate >= 10 else (10 if savings_rate > 0 else 0))
    
    budget_adherence_score = 25
    if not budgets.empty:
        for _, budget in budgets.iterrows():
            spent = current_month_expenses[current_month_expenses['category'] == budget['category']]['amount'].sum()
            if spent > budget['limit']:
                budget_adherence_score -= 5
        budget_adherence_score = max(0, budget_adherence_score)
    else:
        budget_adherence_score = 0

    income_vs_expenses_score = 25 if total_income > total_expenses else (10 if total_income == total_expenses else 5)
    debt_management_score = 20 # Placeholder

    total_score = savings_score + budget_adherence_score + income_vs_expenses_score + debt_management_score
    st.metric("Overall Score", f"{total_score}/100")
    st.progress(total_score / 100)

def smart_assistant_page():
    st.title("🤖 Smart Financial Assistant")

    if st.button("Get Personalized Advice"):
        transactions = load_transactions()
        if not transactions.empty:
            end_date = datetime.now()
            start_date = end_date - pd.Timedelta(days=30)
            recent_transactions = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]
            
            total_income = recent_transactions[recent_transactions["type"] == "income"]["amount"].sum()
            total_expenses = recent_transactions[recent_transactions["type"] == "expense"]["amount"].sum()
            spending_by_category = recent_transactions[recent_transactions["type"] == "expense"].groupby("category")["amount"].sum()

            prompt = f"""
As a friendly financial assistant, analyze the following financial summary and provide 3-5 actionable, personalized recommendations. The user is trying to improve their financial health.

**Financial Summary (Last 30 Days):**
- **Total Income:** {total_income/100:.2f}
- **Total Expenses:** {total_expenses/100:.2f}
- **Spending by Category:**
"""
            if total_expenses > 0:
                for category, amount in spending_by_category.items():
                    percentage = (amount / total_expenses) * 100
                    prompt += f"  - {category}: {amount/100:.2f} ({percentage:.2f}%)\n"
            else:
                prompt += "  - No expenses recorded.\n"
            prompt += "\n**Your Recommendations:**"

            # Simulated LLM Response
            simulated_llm_response = """
1.  **Review Your Food Spending:** Your spending on food seems quite high. Look for opportunities to cook at home more often.
2.  **Create a Shopping Budget:** Your shopping expenses are also significant. Consider setting a specific budget for shopping each month.
3.  **Increase Your Savings:** With your current income and expenses, you have an opportunity to save more. Try to set a savings goal.
"""
            st.markdown(prompt)
            st.subheader("Personalized Recommendations")
            st.markdown(simulated_llm_response)
        else:
            st.info("No transactions found to generate advice.")

def data_management_page():
    st.title("💾 Data Management")

    st.subheader("Export Data")
    export_format = st.selectbox("Export Format", ["CSV", "JSON"])
    if st.button("Export Data"):
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)
        
        transactions = load_transactions()
        budgets = load_budgets()

        if export_format == "CSV":
            export_path = EXPORT_DIR / "export.csv"
            try:
                with open(export_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["type", "date", "category", "description", "amount"])
                    for _, t in transactions.iterrows():
                        writer.writerow(["transaction", t["date"].strftime("%Y-%m-%d"), t["category"], t["description"], t["amount"]])
                    for _, b in budgets.iterrows():
                        writer.writerow(["budget", "", b["category"], "", b["limit"]])
                st.success(f"Data successfully exported to {export_path}")
            except IOError as e:
                st.error(f"Error exporting data to CSV: {e}")

        elif export_format == "JSON":
            export_path = EXPORT_DIR / "export.json"
            data_to_export = {
                "transactions": transactions.to_dict(orient="records"),
                "budgets": budgets.to_dict(orient="records")
            }
            try:
                with open(export_path, "w") as f:
                    json.dump(data_to_export, f, indent=4, default=str)
                st.success(f"Data successfully exported to {export_path}")
            except IOError as e:
                st.error(f"Error exporting data to JSON: {e}")

    st.markdown("---")
    st.subheader("Import Data")
    uploaded_file = st.file_uploader("Choose a file to import (.csv or .json)")

    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        try:
            if file_extension == ".csv":
                # Process CSV
                st.info("CSV import processing to be implemented.")
            elif file_extension == ".json":
                # Process JSON
                st.info("JSON import processing to be implemented.")
            else:
                st.error("Unsupported file format. Please use .csv or .json.")
        except Exception as e:
            st.error(f"An error occurred during import: {e}")

# --- Main App ---
def main():
    st.set_page_config(page_title="Finance Tracker", layout="wide")

    transactions = load_transactions()
    budgets = load_budgets()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Transactions", "Budgets", "Analytics", "Smart Assistant", "Data Management"])

    if page == "Dashboard":
        dashboard_page(transactions, budgets)
    elif page == "Transactions":
        transactions_page(transactions)
    elif page == "Budgets":
        budgets_page(budgets)
    elif page == "Analytics":
        analytics_page(transactions, budgets)
    elif page == "Smart Assistant":
        smart_assistant_page()
    elif page == "Data Management":
        data_management_page()

if __name__ == "__main__":
    main()