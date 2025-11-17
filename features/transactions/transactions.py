import questionary
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

# Constants
TRANSACTIONS_FILE = "database/transactions.txt"
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]

console = Console()

def load_transactions():
    """
    Reads all transactions from the file.
    """
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                date, type, category, description, amount = line.strip().split(",")
                transactions.append({
                    "date": datetime.strptime(date, "%Y-%m-%d"),
                    "type": type,
                    "category": category,
                    "description": description,
                    "amount": int(amount)
                })
    except FileNotFoundError:
        return []
    except Exception as e:
        console.print(f"[bold red]Error reading transactions: {e}[/bold red]")
        return []
    return transactions

def add_transaction(transaction_type):
    """
    Adds a new transaction (expense or income) by prompting the user for details.
    """
    if transaction_type == "expense":
        categories = EXPENSE_CATEGORIES
        color = "red"
    else:
        categories = INCOME_CATEGORIES
        color = "green"

    amount_str = questionary.text(f"Enter the amount for the {transaction_type}:").ask()
    try:
        amount = int(float(amount_str) * 100)  # Store as integer (paisa/cents)
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    category = questionary.select(f"Select a category for the {transaction_type}:", choices=categories).ask()
    description = questionary.text("Enter a description:").ask()
    date_str = questionary.text("Enter the date (YYYY-MM-DD), leave empty for today:", default=datetime.now().strftime("%Y-%m-%d")).ask()

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
        return

    try:
        with open(TRANSACTIONS_FILE, "a") as f:
            f.write(f"{date},{transaction_type},{category},{description},{amount}\n")
        console.print(f"[bold {color}]Successfully added {transaction_type}: {description} ({amount/100:.2f})[/bold {color}]")
    except IOError as e:
        console.print(f"[bold red]Error saving transaction: {e}[/bold red]")

def add_expense():
    """
    Wrapper function to add an expense.
    """
    add_transaction("expense")

def add_income():
    """
    Wrapper function to add an income.
    """
    add_transaction("income")

def list_transactions(days=None):
    """
    Lists all transactions in a table, with optional filtering by days.
    """
    transactions = load_transactions()
    if not transactions:
        console.print("[bold yellow]No transactions found.[/bold yellow]")
        return

    if days:
        transactions = [t for t in transactions if t["date"] >= datetime.now() - timedelta(days=days)]

    transactions.sort(key=lambda t: t["date"], reverse=True)

    table = Table(title="Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="blue")
    table.add_column("Amount", justify="right", style="bold")

    for transaction in transactions:
        color = "red" if transaction["type"] == "expense" else "green"
        table.add_row(
            transaction["date"].strftime("%Y-%m-%d"),
            transaction["type"],
            transaction["category"],
            transaction["description"],
            f"[{color}]{transaction['amount']/100:.2f}[/{color}]"
        )

    console.print(table)

def get_balance():
    """
    Calculates and displays the balance for the current month.
    """
    transactions = load_transactions()
    current_month = datetime.now().month
    current_year = datetime.now().year

    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction["date"].month == current_month and transaction["date"].year == current_year:
            if transaction["type"] == "income":
                total_income += transaction["amount"]
            else:
                total_expense += transaction["amount"]

    balance = total_income - total_expense

    console.print(f"Total Income: [green]{total_income/100:.2f}[/green]")
    console.print(f"Total Expense: [red]{total_expense/100:.2f}[/red]")

    balance_color = "green" if balance >= 0 else "red"
    console.print(f"Balance: [{balance_color}]{balance/100:.2f}[/{balance_color}]")
