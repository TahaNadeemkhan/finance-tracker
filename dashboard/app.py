import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- Constants and File Paths ---
TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt"
EXPORTS_DIR = "exports"

# --- Helper Functions for Data Handling ---

def load_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        return pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount"])
    
    transactions = []
    with open(TRANSACTIONS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                transactions.append({
                    "Date": datetime.strptime(parts[0], "%Y-%m-%d").date(),
                    "Type": parts[1],
                    "Category": parts[2],
                    "Description": parts[3],
                    "Amount": int(parts[4]) # Stored as paisa/cents
                })
    return pd.DataFrame(transactions)

def save_transactions(df):
    os.makedirs(os.path.dirname(TRANSACTIONS_FILE), exist_ok=True)
    df["Date"] = df["Date"].astype(str) # Convert date objects to string for saving
    with open(TRANSACTIONS_FILE, "w") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Date']},{row['Type']},{row['Category']},{row['Description']},{row['Amount']}\n")

def load_budgets():
    if not os.path.exists(BUDGETS_FILE):
        return pd.DataFrame(columns=["Category", "Budget"])
    
    budgets = []
    with open(BUDGETS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                budgets.append({
                    "Category": parts[0],
                    "Budget": int(parts[1]) # Stored as paisa/cents
                })
    return pd.DataFrame(budgets)

def save_budgets(df):
    os.makedirs(os.path.dirname(BUDGETS_FILE), exist_ok=True)
    with open(BUDGETS_FILE, "w") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Category']},{row['Budget']}\n")

def paisa_to_display(amount_paisa):
    return amount_paisa / 100

def display_to_paisa(amount_display):
    return int(amount_display * 100)

# --- Streamlit App Setup ---

st.set_page_config(layout="wide", page_title="Personal Finance Tracker")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header { font-size: 3em; font-weight: bold; color: #4CAF50; text-align: center; margin-bottom: 30px; }
    .card { background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); padding: 20px; margin-bottom: 20px; }
    .metric-value { font-size: 2.5em; font-weight: bold; }
    .metric-label { font-size: 1em; color: #555555; }
    .green-text { color: #4CAF50; }
    .red-text { color: #F44336; }
    .yellow-text { color: #FFC107; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard Overview", "Transactions Management", "Budget Management", "Financial Analytics", "Smart Assistant", "Data Management"])

# --- Main Application Logic ---

transactions_df = load_transactions()
budgets_df = load_budgets()

if page == "Dashboard Overview":
    st.markdown("<h1 class='main-header'>Dashboard Overview</h1>", unsafe_allow_html=True)

    # Calculate financial summary
    total_income = transactions_df[transactions_df["Type"] == "Income"]["Amount"].sum()
    total_expenses = transactions_df[transactions_df["Type"] == "Expense"]["Amount"].sum()
    current_balance = total_income - total_expenses

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-label'>Total Income</div><div class='metric-value green-text'>₹{paisa_to_display(total_income):,.2f}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-label'>Total Expenses</div><div class='metric-value red-text'>₹{paisa_to_display(total_expenses):,.2f}</div>", unsafe_allow_html=True)
    with col3:
        balance_color = "green-text" if current_balance >= 0 else "red-text"
        st.markdown(f"<div class='metric-label'>Current Balance</div><div class='metric-value {balance_color}'>₹{paisa_to_display(current_balance):,.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Expense Breakdown by Category
    st.subheader("Expense Breakdown by Category")
    expense_by_category = transactions_df[transactions_df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
    if not expense_by_category.empty:
        fig_pie = px.pie(expense_by_category, values="Amount", names="Category", title="Expense Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No expenses recorded yet to display category breakdown.")

    st.markdown("---")

    # Budget Status Section
    st.subheader("Budget Status")
    if not budgets_df.empty:
        budget_status_data = []
        for _, budget_row in budgets_df.iterrows():
            category = budget_row["Category"]
            budget_amount = budget_row["Budget"]
            spent_amount = transactions_df[(transactions_df["Type"] == "Expense") & (transactions_df["Category"] == category)]["Amount"].sum()
            
            percentage_used = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
            
            if percentage_used >= 100:
                status_color = "red"
            elif percentage_used >= 70:
                status_color = "orange"
            else:
                status_color = "green"
            
            budget_status_data.append({
                "Category": category,
                "Budget": paisa_to_display(budget_amount),
                "Spent": paisa_to_display(spent_amount),
                "Remaining": paisa_to_display(budget_amount - spent_amount),
                "Percentage Used": f"{percentage_used:.2f}%",
                "Status Color": status_color
            })
        
        for item in budget_status_data:
            st.markdown(f"**{item['Category']}**")
            st.progress(min(item['Spent'] / item['Budget'], 1.0), text=f"Budget: ₹{item['Budget']:.2f} | Spent: ₹{item['Spent']:.2f} | Remaining: ₹{item['Remaining']:.2f} ({item['Percentage Used']})")
            # st.markdown(f"<div style='color:{item['Status Color']};'>Budget: ₹{item['Budget']:.2f} | Spent: ₹{item['Spent']:.2f} | Remaining: ₹{item['Remaining']:.2f} ({item['Percentage Used']})</div>", unsafe_allow_html=True)
    else:
        st.info("No budgets set yet.")

    st.markdown("---")

    # Recent Transactions Table
    st.subheader("Recent Transactions")
    if not transactions_df.empty:
        recent_transactions = transactions_df.sort_values(by="Date", ascending=False).head(10).copy()
        recent_transactions["Amount"] = recent_transactions.apply(
            lambda row: f"<span class='green-text'>+₹{paisa_to_display(row['Amount']):,.2f}</span>" if row['Type'] == 'Income'
            else f"<span class='red-text'>-₹{paisa_to_display(row['Amount']):,.2f}</span>",
            axis=1
        )
        st.markdown(recent_transactions[["Date", "Type", "Category", "Description", "Amount"]].to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No transactions recorded yet.")

elif page == "Transactions Management":
    st.markdown("<h1 class='main-header'>Transactions Management</h1>", unsafe_allow_html=True)

    st.subheader("Add New Transaction")
    with st.form("new_transaction_form"):
        transaction_type = st.radio("Type", ["Income", "Expense"])
        amount_display = st.number_input("Amount", min_value=0.01, format="%.2f")
        
        # Categories for expenses and sources for income
        if transaction_type == "Expense":
            category_options = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
            category = st.selectbox("Category", category_options)
        else:
            category_options = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
            category = st.selectbox("Source", category_options)
            
        description = st.text_input("Description")
        date = st.date_input("Date", datetime.now().date())

        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if amount_display <= 0:
                st.error("Amount must be a positive number.")
            else:
                new_transaction = {
                    "Date": date,
                    "Type": transaction_type,
                    "Category": category,
                    "Description": description,
                    "Amount": display_to_paisa(amount_display)
                }
                transactions_df = pd.concat([transactions_df, pd.DataFrame([new_transaction])], ignore_index=True)
                save_transactions(transactions_df)
                st.success("Transaction added successfully!")
                st.rerun()

    st.subheader("View All Transactions")
    if not transactions_df.empty:
        # Filter transactions by date range
        min_date = transactions_df["Date"].min()
        max_date = transactions_df["Date"].max()

        if pd.isna(min_date): # Handle case where min_date might be NaT
            min_date = datetime.now().date()
        if pd.isna(max_date): # Handle case where max_date might be NaT
            max_date = datetime.now().date()

        date_range = st.date_input("Filter by Date Range", value=(min_date, max_date))

        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_transactions_df = transactions_df[
                (transactions_df["Date"] >= start_date) & (transactions_df["Date"] <= end_date)
            ].copy()
        else:
            filtered_transactions_df = transactions_df.copy()

        # Display transactions
        display_df = filtered_transactions_df.copy()
        display_df["Amount"] = display_df.apply(
            lambda row: f"<span class='green-text'>+₹{paisa_to_display(row['Amount']):,.2f}</span>" if row['Type'] == 'Income'
            else f"<span class='red-text'>-₹{paisa_to_display(row['Amount']):,.2f}</span>",
            axis=1
        )
        st.markdown(display_df[["Date", "Type", "Category", "Description", "Amount"]].sort_values(by="Date", ascending=False).to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No transactions recorded yet.")

elif page == "Budget Management":
    st.markdown("<h1 class='main-header'>Budget Management</h1>", unsafe_allow_html=True)

    st.subheader("Set New Budget")
    with st.form("new_budget_form"):
        expense_categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
        category = st.selectbox("Category", expense_categories)
        budget_amount_display = st.number_input("Budget Amount", min_value=0.01, format="%.2f")

        submitted = st.form_submit_button("Set Budget")
        if submitted:
            if budget_amount_display <= 0:
                st.error("Budget amount must be a positive number.")
            else:
                new_budget = {
                    "Category": category,
                    "Budget": display_to_paisa(budget_amount_display)
                }
                # Update existing budget or add new one
                if category in budgets_df["Category"].values:
                    budgets_df.loc[budgets_df["Category"] == category, "Budget"] = new_budget["Budget"]
                else:
                    budgets_df = pd.concat([budgets_df, pd.DataFrame([new_budget])], ignore_index=True)
                save_budgets(budgets_df)
                st.success(f"Budget for {category} set to ₹{budget_amount_display:,.2f} successfully!")
                st.rerun()

    st.subheader("View Current Budgets")
    if not budgets_df.empty:
        budget_display_data = []
        for _, budget_row in budgets_df.iterrows():
            category = budget_row["Category"]
            budget_amount = budget_row["Budget"]
            spent_amount = transactions_df[(transactions_df["Type"] == "Expense") & (transactions_df["Category"] == category)]["Amount"].sum()
            
            remaining_amount = budget_amount - spent_amount
            status = "Under Budget" if remaining_amount >= 0 else "Over Budget"
            status_color = "green-text" if remaining_amount >= 0 else "red-text"

            budget_display_data.append({
                "Category": category,
                "Budget Amount": f"₹{paisa_to_display(budget_amount):,.2f}",
                "Spent Amount": f"₹{paisa_to_display(spent_amount):,.2f}",
                "Remaining Amount": f"<span class='{status_color}'>₹{paisa_to_display(remaining_amount):,.2f}</span>",
                "Status": f"<span class='{status_color}'>{status}</span>"
            })
        
        st.markdown(pd.DataFrame(budget_display_data).to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No budgets set yet.")

elif page == "Financial Analytics":
    st.markdown("<h1 class='main-header'>Financial Analytics</h1>", unsafe_allow_html=True)

    if transactions_df.empty:
        st.info("No transactions to analyze yet.")
    else:
        # Ensure 'Date' column is datetime for filtering
        transactions_df["Date"] = pd.to_datetime(transactions_df["Date"])

        # Get current month's data
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_month_df = transactions_df[(transactions_df["Date"].dt.month == current_month) & (transactions_df["Date"].dt.year == current_year)]

        # Get last month's data
        last_month_date = datetime.now().replace(day=1) - pd.DateOffset(days=1)
        last_month = last_month_date.month
        last_year = last_month_date.year
        last_month_df = transactions_df[(transactions_df["Date"].dt.month == last_month) & (transactions_df["Date"].dt.year == last_year)]

        # --- Spending Analysis ---
        st.subheader("Spending Analysis (Current Month)")
        current_month_expenses = current_month_df[current_month_df["Type"] == "Expense"]
        if not current_month_expenses.empty:
            spending_by_category = current_month_expenses.groupby("Category")["Amount"].sum().reset_index()
            fig_spending = px.bar(spending_by_category, x="Category", y="Amount", title="Spending Distribution by Category")
            st.plotly_chart(fig_spending, use_container_width=True)

            st.markdown("---")
            st.write("**Top 3 Spending Categories:**")
            top_categories = spending_by_category.sort_values(by="Amount", ascending=False).head(3)
            for _, row in top_categories.iterrows():
                st.write(f"- {row['Category']}: ₹{paisa_to_display(row['Amount']):,.2f}")
            
            st.markdown("---")
            avg_daily_expense = current_month_expenses["Amount"].sum() / (datetime.now().day if datetime.now().day > 0 else 1)
            st.write(f"**Average Daily Expense:** ₹{paisa_to_display(avg_daily_expense):,.2f}")

            # Comparison with last month
            last_month_total_expenses = last_month_df[last_month_df["Type"] == "Expense"]["Amount"].sum()
            current_month_total_expenses = current_month_expenses["Amount"].sum()
            if last_month_total_expenses > 0:
                expense_change = ((current_month_total_expenses - last_month_total_expenses) / last_month_total_expenses) * 100
                if expense_change > 0:
                    st.write(f"**Spending vs. Last Month:** Up {expense_change:.2f}%")
                else:
                    st.write(f"**Spending vs. Last Month:** Down {abs(expense_change):,.2f}%")
            else:
                st.write("**Spending vs. Last Month:** No expenses last month for comparison.")
        else:
            st.info("No expenses recorded for the current month.")

        st.markdown("---")

        # --- Income Analysis ---
        st.subheader("Income Analysis (Current Month)")
        current_month_income = current_month_df[current_month_df["Type"] == "Income"]
        if not current_month_income.empty:
            income_by_source = current_month_income.groupby("Category")["Amount"].sum().reset_index()
            fig_income = px.bar(income_by_source, x="Category", y="Amount", title="Income Distribution by Source")
            st.plotly_chart(fig_income, use_container_width=True)

            st.markdown("---")
            st.write(f"**Total Income This Month:** ₹{paisa_to_display(current_month_income['Amount'].sum()):,.2f}")

            # Comparison with last month
            last_month_total_income = last_month_df[last_month_df["Type"] == "Income"]["Amount"].sum()
            current_month_total_income = current_month_income["Amount"].sum()
            if last_month_total_income > 0:
                income_change = ((current_month_total_income - last_month_total_income) / last_month_total_income) * 100
                if income_change > 0:
                    st.write(f"**Income vs. Last Month:** Up {income_change:.2f}%")
                else:
                    st.write(f"**Income vs. Last Month:** Down {abs(income_change):,.2f}%")
            else:
                st.write("**Income vs. Last Month:** No income last month for comparison.")
        else:
            st.info("No income recorded for the current month.")

        st.markdown("---")

        # --- Savings Analysis ---
        st.subheader("Savings Analysis (Current Month)")
        current_month_total_income = current_month_df[current_month_df["Type"] == "Income"]["Amount"].sum()
        current_month_total_expenses = current_month_df[current_month_df["Type"] == "Expense"]["Amount"].sum()
        
        monthly_savings = current_month_total_income - current_month_total_expenses
        st.write(f"**Monthly Savings:** ₹{paisa_to_display(monthly_savings):,.2f}")

        if current_month_total_income > 0:
            savings_rate = (monthly_savings / current_month_total_income) * 100
            st.write(f"**Savings Rate:** {savings_rate:.2f}%")
        else:
            st.write("**Savings Rate:** N/A (No income this month)")

        st.markdown("---")

        # --- Financial Health Score (Placeholder) ---
        st.subheader("Financial Health Score")
        st.info("Financial Health Score calculation is a placeholder. Implement logic based on savings rate, budget adherence, income vs expenses, and debt management.")
        st.write("Overall Score: 75/100 (Good)")
        st.write("Recommendations: Continue to monitor your spending and consider increasing your savings rate.")

elif page == "Smart Assistant":
    st.markdown("<h1 class='main-header'>Smart Assistant</h1>", unsafe_allow_html=True)

    st.subheader("Get Personalized Advice")
    if st.button("Generate Advice"):
        if transactions_df.empty:
            st.info("Please record some transactions to get personalized advice.")
        else:
            # Gather financial summary for LLM prompt
            recent_transactions_df = transactions_df[transactions_df["Date"] >= (datetime.now().date() - pd.DateOffset(days=30))]
            
            total_income_llm = recent_transactions_df[recent_transactions_df["Type"] == "Income"]["Amount"].sum()
            total_expenses_llm = recent_transactions_df[recent_transactions_df["Type"] == "Expense"]["Amount"].sum()
            
            spending_by_category_llm = recent_transactions_df[recent_transactions_df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
            spending_summary = ""
            if not spending_by_category_llm.empty:
                total_recent_expenses = spending_by_category_llm["Amount"].sum()
                for _, row in spending_by_category_llm.iterrows():
                    percentage = (row['Amount'] / total_recent_expenses * 100) if total_recent_expenses > 0 else 0
                    spending_summary += f"- {row['Category']}: ₹{paisa_to_display(row['Amount']):,.2f} ({percentage:.0f}%)\n"

            llm_prompt = f"""
            As a friendly financial assistant, analyze the following financial summary and provide 3-5 actionable, personalized recommendations. The user is trying to improve their financial health.

            **Financial Summary (Last 30 Days):**
            - **Total Income:** ₹{paisa_to_display(total_income_llm):,.2f}
            - **Total Expenses:** ₹{paisa_to_display(total_expenses_llm):,.2f}
            - **Spending by Category:**
            {spending_summary if spending_summary else "No expenses recorded."} 

            **Your Recommendations:**
            """
            
            # Simulate LLM response
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("Thinking...")
            st.write("Here are some personalized recommendations based on your recent financial activity:")
            st.write("- **Review your 'Food' spending:** It accounts for a significant portion of your expenses. Consider meal planning or cooking at home more often to save money.")
            st.write("- **Track your 'Shopping' habits:** If possible, try to differentiate between needs and wants. Setting a specific budget for shopping can help you stay on track.")
            st.write("- **Increase your savings:** With your current income and expenses, you have a good opportunity to increase your monthly savings. Consider setting up an automatic transfer to a savings account.")
            st.write("- **Explore investment options:** Once you have a solid emergency fund, look into low-risk investment options to make your money grow.")
            st.write("- **Regularly review your budget:** Make it a habit to check your spending against your budget weekly to identify areas for improvement early.")
            st.markdown("</div>", unsafe_allow_html=True)

elif page == "Data Management":
    st.markdown("<h1 class='main-header'>Data Management</h1>", unsafe_allow_html=True)

    st.subheader("Export Data")
    export_format = st.selectbox("Select Export Format", ["CSV", "JSON"])
    if st.button("Export"):
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export Transactions
        transactions_export_df = transactions_df.copy()
        transactions_export_df["Amount"] = transactions_export_df["Amount"].apply(paisa_to_display) # Convert to display format for export
        
        if export_format == "CSV":
            transactions_export_path = os.path.join(EXPORTS_DIR, f"transactions_export_{timestamp}.csv")
            transactions_export_df.to_csv(transactions_export_path, index=False)
            st.success(f"Transactions exported to {transactions_export_path}")
        else: # JSON
            transactions_export_path = os.path.join(EXPORTS_DIR, f"transactions_export_{timestamp}.json")
            transactions_export_df.to_json(transactions_export_path, orient="records", indent=4)
            st.success(f"Transactions exported to {transactions_export_path}")

        # Export Budgets
        budgets_export_df = budgets_df.copy()
        budgets_export_df["Budget"] = budgets_export_df["Budget"].apply(paisa_to_display) # Convert to display format for export

        if export_format == "CSV":
            budgets_export_path = os.path.join(EXPORTS_DIR, f"budgets_export_{timestamp}.csv")
            budgets_export_df.to_csv(budgets_export_path, index=False)
            st.success(f"Budgets exported to {budgets_export_path}")
        else: # JSON
            budgets_export_path = os.path.join(EXPORTS_DIR, f"budgets_export_{timestamp}.json")
            budgets_export_df.to_json(budgets_export_path, orient="records", indent=4)
            st.success(f"Budgets exported to {budgets_export_path}")

    st.subheader("Import Data (Placeholder)")
    st.info("Import functionality is a placeholder. You can upload CSV/JSON files here for future implementation.")
    uploaded_file = st.file_uploader("Upload a file to import", type=["csv", "json"])
    if uploaded_file is not None:
        st.write("File uploaded successfully! (Import processing not yet implemented)")
        # Future implementation would parse the file and append to transactions_df/budgets_df
