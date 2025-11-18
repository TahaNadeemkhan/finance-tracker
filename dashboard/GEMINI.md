# Day 7: Web Dashboard & Final Polish

## Today's Objective
This document describes the features and functionality of the existing Streamlit web dashboard for the Personal Finance Tracker CLI. It provides a visual interface to interact with and analyze your financial data.

---

## Part A: Streamlit Web Dashboard Features

### Tech Stack
- **Streamlit** - Python web framework for building interactive web applications.
- **Pandas** - For data manipulation and analysis.
- **Plotly Express** - For generating interactive charts and visualizations.

### Implemented Features

The Streamlit dashboard provides the following pages, accessible via the sidebar navigation:

#### 1. Dashboard Overview
- **Financial Summary**: Displays key metrics including:
    - Total Income
    - Total Expenses
    - Current Balance
- **Expense Breakdown by Category**: An interactive pie chart visualizing the distribution of expenses across different categories.
- **Budgets vs. Actual Spending**: A bar chart comparing set budget limits against actual spending for each category.

#### 2. Transactions Management
- **Add New Transaction**: A form to record new income or expense transactions, including:
    - Type (Income/Expense)
    - Amount
    - Category/Source
    - Description
    - Date
- **View All Transactions**: A table displaying all recorded transactions.
- **Filter Transactions**: Functionality to filter transactions by a custom date range.

#### 3. Budget Management
- **Set New Budget**: A form to define or update budget limits for specific expense categories.
- **View Current Budgets**: A table listing all set budgets with their respective limits.

#### 4. Financial Analytics
- **Spending Analysis**: Bar chart showing spending distribution by category for the current month.
- **Income Analysis**: Bar chart showing income distribution by source for the current month.
- **Savings Analysis**: Displays monthly savings amount and calculated savings rate.
- **Financial Health Score**: Calculates and presents an overall financial health score based on:
    - Savings rate
    - Budget adherence
    - Income vs. expenses
    - (Placeholder for Debt management)

#### 5. Smart Assistant
- **Get Personalized Advice**: Gathers a summary of recent financial activity and uses it to generate (simulated) personalized financial recommendations. This demonstrates integration with an LLM for financial insights.

#### 6. Data Management
- **Export Data**: Allows users to export their transaction and budget data into either CSV or JSON format.
- **Import Data**: Provides an interface to upload CSV or JSON files for importing data (import processing is currently a placeholder for future implementation).

### Data Handling
- All monetary values are handled as integers (paisa/cents) to prevent floating-point inaccuracies.
- Amounts are displayed in Pakistani Rupees (PKR).
- Data is loaded from and saved to `transactions.txt` and `budgets.txt` files.
- Exported files are saved in the `exports` directory.
