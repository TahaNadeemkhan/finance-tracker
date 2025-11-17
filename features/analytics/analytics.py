import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timedelta
import os
from features.transactions.transactions import load_transactions, EXPENSE_CATEGORIES
from features.budgets.budgets import load_budgets

console = Console()

FINANCIAL_ANALYTICS_FILE = os.path.join("database", "financial_analytics.txt")

def spending_analysis():
    """
    Calculates and displays spending breakdown by category, top 3 spending categories,
    average daily expense, comparison with last month, and spending trends.
    """
    console.print(Panel("[bold blue]Spending Analysis[/bold blue]", expand=False))
    
    transactions = load_transactions()
    budgets = load_budgets()

    if not transactions:
        console.print("[bold yellow]No transactions found for analysis.[/bold yellow]")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Filter transactions for the current month and expenses only
    current_month_expenses = [
        t for t in transactions 
        if t["date"].month == current_month and 
           t["date"].year == current_year and 
           t["type"] == "expense"
    ]

    if not current_month_expenses:
        console.print("[bold yellow]No expenses recorded for the current month.[/bold yellow]")
        return

    # Spending breakdown by category
    spending_by_category = {category: 0 for category in EXPENSE_CATEGORIES}
    total_expenses_current_month = 0

    for t in current_month_expenses:
        if t["category"] in spending_by_category:
            spending_by_category[t["category"]] += t["amount"]
        total_expenses_current_month += t["amount"]

    console.print("\n[bold underline]Spending Breakdown by Category (Current Month):[/bold underline]")
    if total_expenses_current_month > 0:
        for category, amount in spending_by_category.items():
            percentage = (amount / total_expenses_current_month) * 100
            console.print(f"{category}: {amount/100:.2f} ({percentage:.2f}%)")
    else:
        console.print("No expenses to categorize.")

    # Top 3 spending categories
    sorted_spending = sorted(spending_by_category.items(), key=lambda item: item[1], reverse=True)
    console.print("\n[bold underline]Top 3 Spending Categories (Current Month):[/bold underline]")
    for category, amount in sorted_spending[:3]:
        if amount > 0:
            console.print(f"- {category}: {amount/100:.2f}")
    
    # Average daily expense
    days_in_month = (datetime(current_year, current_month % 12 + 1, 1) - datetime(current_year, current_month, 1)).days
    average_daily_expense = total_expenses_current_month / days_in_month if days_in_month > 0 else 0
    console.print(f"\n[bold underline]Average Daily Expense (Current Month):[/bold underline] {average_daily_expense/100:.2f}")

    # Comparison with last month
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1

    last_month_expenses = [
        t for t in transactions 
        if t["date"].month == last_month and 
           t["date"].year == last_month_year and 
           t["type"] == "expense"
    ]
    total_expenses_last_month = sum(t["amount"] for t in last_month_expenses)

    console.print("\n[bold underline]Comparison with Last Month:[/bold underline]")
    console.print(f"Total Expenses Current Month: {total_expenses_current_month/100:.2f}")
    console.print(f"Total Expenses Last Month: {total_expenses_last_month/100:.2f}")
    
    if total_expenses_last_month > 0:
        change = ((total_expenses_current_month - total_expenses_last_month) / total_expenses_last_month) * 100
        if change > 0:
            console.print(f"Spending increased by [red]{change:.2f}%[/red] compared to last month.")
        elif change < 0:
            console.print(f"Spending decreased by [green]{abs(change):.2f}%[/green] compared to last month.")
        else:
            console.print("Spending remained the same as last month.")
    else:
        console.print("No expenses last month for comparison.")

    # Spending trends (simple: compare last 3 months)
    console.print("\n[bold underline]Spending Trends (Last 3 Months):[/bold underline]")
    monthly_spending = {}
    for i in range(3):
        month = current_month - i
        year = current_year
        if month <= 0:
            month += 12
            year -= 1
        
        month_expenses = [
            t for t in transactions 
            if t["date"].month == month and 
               t["date"].year == year and 
               t["type"] == "expense"
        ]
        total_month_expense = sum(t["amount"] for t in month_expenses)
        monthly_spending[f"{year}-{month:02d}"] = total_month_expense
    
    sorted_months = sorted(monthly_spending.keys())
    for month_year in sorted_months:
        console.print(f"{month_year}: {monthly_spending[month_year]/100:.2f}")

    # TODO: Implement spending analysis logic

def income_analysis():
    """
    Calculates and displays income by source, total income this month,
    comparison with last month, and income stability.
    """
    console.print(Panel("[bold green]Income Analysis[/bold green]", expand=False))
    
    transactions = load_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found for analysis.[/bold yellow]")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter transactions for the current month and income only
    current_month_income = [
        t for t in transactions 
        if t["date"].month == current_month and 
           t["date"].year == current_year and 
           t["type"] == "income"
    ]

    if not current_month_income:
        console.print("[bold yellow]No income recorded for the current month.[/bold yellow]")
        return

    # Income by source
    income_by_source = {}
    total_income_current_month = 0

    for t in current_month_income:
        source = t["category"] # Assuming category is the source for income
        income_by_source[source] = income_by_source.get(source, 0) + t["amount"]
        total_income_current_month += t["amount"]

    console.print("\n[bold underline]Income by Source (Current Month):[/bold underline]")
    for source, amount in income_by_source.items():
        console.print(f"- {source}: {amount/100:.2f}")

    console.print(f"\n[bold underline]Total Income (Current Month):[/bold underline] {total_income_current_month/100:.2f}")

    # Comparison with last month
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1

    last_month_income = [
        t for t in transactions 
        if t["date"].month == last_month and 
           t["date"].year == last_month_year and 
           t["type"] == "income"
    ]
    total_income_last_month = sum(t["amount"] for t in last_month_income)

    console.print("\n[bold underline]Comparison with Last Month:[/bold underline]")
    console.print(f"Total Income Current Month: {total_income_current_month/100:.2f}")
    console.print(f"Total Income Last Month: {total_income_last_month/100:.2f}")
    
    if total_income_last_month > 0:
        change = ((total_income_current_month - total_income_last_month) / total_income_last_month) * 100
        if change > 0:
            console.print(f"Income increased by [green]{change:.2f}%[/green] compared to last month.")
        elif change < 0:
            console.print(f"Income decreased by [red]{abs(change):.2f}%[/red] compared to last month.")
        else:
            console.print("Income remained the same as last month.")
    else:
        console.print("No income last month for comparison.")

    # Income stability (simple: compare last 3 months)
    console.print("\n[bold underline]Income Trends (Last 3 Months):[/bold underline]")
    monthly_income = {}
    for i in range(3):
        month = current_month - i
        year = current_year
        if month <= 0:
            month += 12
            year -= 1
        
        month_income_transactions = [
            t for t in transactions 
            if t["date"].month == month and 
               t["date"].year == year and 
               t["type"] == "income"
        ]
        total_month_income = sum(t["amount"] for t in month_income_transactions)
        monthly_income[f"{year}-{month:02d}"] = total_month_income
    
    sorted_months = sorted(monthly_income.keys())
    for month_year in sorted_months:
        console.print(f"{month_year}: {monthly_income[month_year]/100:.2f}")

def savings_analysis():
    """
    Calculates and displays monthly savings amount, savings rate,
    savings trend, and savings goal progress.
    """
    console.print(Panel("[bold yellow]Savings Analysis[/bold yellow]", expand=False))
    
    transactions = load_transactions()

    if not transactions:
        console.print("[bold yellow]No transactions found for analysis.[/bold yellow]")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year

    total_income_current_month = 0
    total_expenses_current_month = 0

    for t in transactions:
        if t["date"].month == current_month and t["date"].year == current_year:
            if t["type"] == "income":
                total_income_current_month += t["amount"]
            else:
                total_expenses_current_month += t["amount"]

    monthly_savings = total_income_current_month - total_expenses_current_month
    console.print(f"\n[bold underline]Monthly Savings (Current Month):[/bold underline] {monthly_savings/100:.2f}")

    # Savings rate
    savings_rate = (monthly_savings / total_income_current_month) * 100 if total_income_current_month > 0 else 0
    console.print(f"[bold underline]Savings Rate (Current Month):[/bold underline] {savings_rate:.2f}%")

    # Savings trend (last 3 months)
    console.print("\n[bold underline]Savings Trends (Last 3 Months):[/bold underline]")
    monthly_savings_trend = {}
    for i in range(3):
        month = current_month - i
        year = current_year
        if month <= 0:
            month += 12
            year -= 1
        
        month_income = 0
        month_expenses = 0
        for t in transactions:
            if t["date"].month == month and t["date"].year == year:
                if t["type"] == "income":
                    month_income += t["amount"]
                else:
                    month_expenses += t["amount"]
        
        monthly_savings_trend[f"{year}-{month:02d}"] = month_income - month_expenses
    
    sorted_months = sorted(monthly_savings_trend.keys())
    for month_year in sorted_months:
        console.print(f"{month_year}: {monthly_savings_trend[month_year]/100:.2f}")

    # Savings goal progress (placeholder - assuming a goal of 100000 paisa for now)
    savings_goal = 100000 # Example goal: 1000.00
    console.print(f"\n[bold underline]Savings Goal Progress:[/bold underline]")
    if monthly_savings >= savings_goal:
        console.print(f"[green]You have reached or exceeded your monthly savings goal of {savings_goal/100:.2f}![/green]")
    else:
        console.print(f"[yellow]You are { (savings_goal - monthly_savings)/100:.2f} away from your monthly savings goal of {savings_goal/100:.2f}.[/yellow]")

def financial_health_score():
    """
    Calculates and displays the financial health score based on savings rate,
    budget adherence, income vs expenses, and debt management.
    Provides recommendations.
    """
    console.print(Panel("[bold magenta]Financial Health Score[/bold magenta]", expand=False))
    
    transactions = load_transactions()
    budgets = load_budgets()

    if not transactions:
        console.print("[bold yellow]No transactions found for analysis. Cannot calculate financial health score.[/bold yellow]")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year

    total_income_current_month = 0
    total_expenses_current_month = 0
    
    for t in transactions:
        if t["date"].month == current_month and t["date"].year == current_year:
            if t["type"] == "income":
                total_income_current_month += t["amount"]
            else:
                total_expenses_current_month += t["amount"]

    # 1. Savings Rate (30 points)
    monthly_savings = total_income_current_month - total_expenses_current_month
    savings_rate = (monthly_savings / total_income_current_month) * 100 if total_income_current_month > 0 else 0
    savings_score = 0
    if savings_rate >= 20:
        savings_score = 30
    elif savings_rate >= 10:
        savings_score = 20
    elif savings_rate > 0:
        savings_score = 10
    
    # 2. Budget Adherence (25 points)
    budget_adherence_score = 25
    if budgets:
        spent_by_category = {category: 0 for category in EXPENSE_CATEGORIES}
        for transaction in transactions:
            if transaction["date"].month == current_month and \
               transaction["date"].year == current_year and \
               transaction["type"] == "expense" and \
               transaction["category"] in spent_by_category:
                spent_by_category[transaction["category"]] += transaction["amount"]
        
        for category, budget_amount in budgets.items():
            spent_amount = spent_by_category.get(category, 0)
            if spent_amount > budget_amount:
                budget_adherence_score -= 5 # Deduct points for each overspent category
                if budget_adherence_score < 0:
                    budget_adherence_score = 0
    else:
        budget_adherence_score = 0 # No budgets set, no score for adherence

    # 3. Income vs Expenses (25 points)
    income_vs_expenses_score = 0
    if total_income_current_month > total_expenses_current_month:
        income_vs_expenses_score = 25
    elif total_income_current_month == total_expenses_current_month:
        income_vs_expenses_score = 10
    else:
        income_vs_expenses_score = 5

    # 4. Debt Management (20 points) - Placeholder, as debt tracking is not implemented
    debt_management_score = 20 # Assuming good debt management for now

    total_score = savings_score + budget_adherence_score + income_vs_expenses_score + debt_management_score

    console.print(f"\n[bold underline]Financial Health Score:[/bold underline] {total_score}/100")

    console.print("\n[bold underline]Score Breakdown:[/bold underline]")
    console.print(f"  Savings Rate: {savings_score} points (Target: 20% savings rate for full points)")
    console.print(f"  Budget Adherence: {budget_adherence_score} points (Stay within budget for full points)")
    console.print(f"  Income vs Expenses: {income_vs_expenses_score} points (Income > Expenses for full points)")
    console.print(f"  Debt Management: {debt_management_score} points (No debt tracking implemented yet)")

    console.print("\n[bold underline]Recommendations:[/bold underline]")
    if total_score >= 80:
        console.print("[green]Excellent! Your financial health is strong. Keep up the great work![/green]")
    elif total_score >= 60:
        console.print("[yellow]Good. You're on the right track, but there's room for improvement. Consider reviewing your spending habits.[/yellow]")
    else:
        console.print("[red]Needs Attention. Your financial health could be better. Focus on increasing savings, adhering to budgets, and managing expenses.[/red]")
    
    if savings_rate < 20 and total_income_current_month > 0:
        console.print("- Try to increase your savings rate. Even small increases can make a big difference.")
    if budget_adherence_score < 25 and budgets:
        console.print("- Review your budget categories and try to stick to your spending limits.")
    if total_income_current_month <= total_expenses_current_month:
        console.print("- Look for ways to increase your income or reduce your expenses to ensure income exceeds expenses.")
    console.print("- Consider implementing debt tracking for a more accurate financial health score.")

def generate_comprehensive_report():
    """
    Generates a comprehensive report including month overview, income summary,
    expense summary, budget performance, savings achieved, top transactions,
    trends, and next month projections.
    """
    console.print(Panel("[bold cyan]Comprehensive Report[/bold cyan]", expand=False))
    
    transactions = load_transactions()
    budgets = load_budgets()

    if not transactions:
        console.print("[bold yellow]No transactions found for report generation.[/bold yellow]")
        return

    current_month = datetime.now().month
    current_year = datetime.now().year

    console.print(f"\n[bold underline]Financial Report for {datetime.now().strftime('%B %Y')}:[/bold underline]")

    total_income_current_month = 0
    total_expenses_current_month = 0
    current_month_expenses = []
    current_month_income = []

    for t in transactions:
        if t["date"].month == current_month and t["date"].year == current_year:
            if t["type"] == "income":
                total_income_current_month += t["amount"]
                current_month_income.append(t)
            else:
                total_expenses_current_month += t["amount"]
                current_month_expenses.append(t)

    # Income Summary
    console.print("\n[bold green]Income Summary:[/bold green]")
    income_by_source = {}
    for t in current_month_income:
        source = t["category"]
        income_by_source[source] = income_by_source.get(source, 0) + t["amount"]
    for source, amount in income_by_source.items():
        console.print(f"- {source}: {amount/100:.2f}")
    console.print(f"Total Income: {total_income_current_month/100:.2f}")

    # Expense Summary
    console.print("\n[bold red]Expense Summary:[/bold red]")
    spending_by_category = {}
    for t in current_month_expenses:
        category = t["category"]
        spending_by_category[category] = spending_by_category.get(category, 0) + t["amount"]
    for category, amount in spending_by_category.items():
        console.print(f"- {category}: {amount/100:.2f}")
    console.print(f"Total Expenses: {total_expenses_current_month/100:.2f}")

    # Budget Performance
    console.print("\n[bold blue]Budget Performance:[/bold blue]")
    if budgets:
        for category, budget_amount in budgets.items():
            spent_amount = spending_by_category.get(category, 0)
            remaining_amount = budget_amount - spent_amount
            status = "Under Budget" if remaining_amount >= 0 else "Over Budget"
            color = "green" if remaining_amount >= 0 else "red"
            console.print(f"- {category}: Budget {budget_amount/100:.2f}, Spent {spent_amount/100:.2f}, Remaining [{color}]{remaining_amount/100:.2f}[/{color}] ({status})")
    else:
        console.print("No budgets set.")

    # Savings Achieved
    monthly_savings = total_income_current_month - total_expenses_current_month
    console.print(f"\n[bold yellow]Savings Achieved:[/bold yellow] {monthly_savings/100:.2f}")

    # Top Transactions (Expenses)
    console.print("\n[bold magenta]Top 3 Expenses:[/bold magenta]")
    sorted_expenses = sorted(current_month_expenses, key=lambda x: x["amount"], reverse=True)
    for t in sorted_expenses[:3]:
        console.print(f"- {t['date'].strftime('%Y-%m-%d')} - {t['description']}: {t['amount']/100:.2f}")

    # Trends (simple overview)
    console.print("\n[bold cyan]Trends Overview:[/bold cyan]")
    console.print("- Refer to 'Spending Analysis' and 'Income Analysis' for detailed trends.")

    # Next Month Projections (simple: based on current month's spending/income)
    console.print("\n[bold white]Next Month Projections (Based on Current Month):[/bold white]")
    console.print(f"- Projected Income: {total_income_current_month/100:.2f}")
    console.print(f"- Projected Expenses: {total_expenses_current_month/100:.2f}")
    console.print(f"- Projected Savings: {monthly_savings/100:.2f}")

def display_financial_analytics_menu():
    """
    Displays the financial analytics menu and handles user choices.
    """
    while True:
        choice = questionary.select(
            "Financial Analytics Menu:",
            choices=[
                "Spending Analysis",
                "Income Analysis",
                "Savings Analysis",
                "Financial Health Score",
                "Generate Comprehensive Report",
                "Back to Main Menu"
            ]
        ).ask()

        if choice == "Spending Analysis":
            spending_analysis()
        elif choice == "Income Analysis":
            income_analysis()
        elif choice == "Savings Analysis":
            savings_analysis()
        elif choice == "Financial Health Score":
            financial_health_score()
        elif choice == "Generate Comprehensive Report":
            generate_comprehensive_report()
        elif choice == "Back to Main Menu":
            break
