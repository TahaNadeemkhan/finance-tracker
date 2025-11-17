import questionary
from rich.console import Console
from rich.table import Table
from features.transactions.transactions import EXPENSE_CATEGORIES, load_transactions
from datetime import datetime

# Constants
BUDGETS_FILE = "database/budgets.txt"

console = Console()

def load_budgets():
    """
    Reads all budgets from the file.
    """
    budgets = {}
    try:
        with open(BUDGETS_FILE, "r") as f:
            for line in f:
                category, amount = line.strip().split(",")
                budgets[category] = int(amount)
    except FileNotFoundError:
        return {}
    except Exception as e:
        console.print(f"[bold red]Error reading budgets: {e}[/bold red]")
        return {}
    return budgets

def set_budget():
    """
    Sets a budget for a specific category.
    """
    category = questionary.select("Select a category to set budget for:", choices=EXPENSE_CATEGORIES).ask()
    if not category:
        return

    amount_str = questionary.text(f"Enter the budget amount for {category}:").ask()
    try:
        amount = int(float(amount_str) * 100)  # Store as integer (paisa/cents)
        if amount <= 0:
            console.print("[bold red]Amount must be a positive number.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    budgets = load_budgets()
    budgets[category] = amount

    try:
        with open(BUDGETS_FILE, "w") as f:
            for cat, amt in budgets.items():
                f.write(f"{cat},{amt}\n")
        console.print(f"[bold green]Budget for {category} set to {amount/100:.2f}[/bold green]")
    except IOError as e:
        console.print(f"[bold red]Error saving budget: {e}[/bold red]")

def view_budgets():
    """
    Displays all set budgets and tracks spending against them for the current month.
    """
    budgets = load_budgets()
    if not budgets:
        console.print("[bold yellow]No budgets set.[/bold yellow]")
        return

    transactions = _get_transactions()
    current_month = datetime.now().month
    current_year = datetime.now().year

    spent_by_category = {category: 0 for category in EXPENSE_CATEGORIES}
    for transaction in transactions:
        if transaction["date"].month == current_month and \
           transaction["date"].year == current_year and \
           transaction["type"] == "expense" and \
           transaction["category"] in spent_by_category:
            spent_by_category[transaction["category"]] += transaction["amount"]

    table = Table(title="Monthly Budgets")
    table.add_column("Category", style="cyan")
    table.add_column("Budget", justify="right", style="magenta")
    table.add_column("Spent", justify="right", style="yellow")
    table.add_column("Remaining", justify="right", style="blue")
    table.add_column("Status", style="bold")

    for category, budget_amount in budgets.items():
        spent_amount = spent_by_category.get(category, 0)
        remaining_amount = budget_amount - spent_amount
        
        status_color = "green" if remaining_amount >= 0 else "red"
        status = "Under Budget" if remaining_amount >= 0 else "Over Budget"

        table.add_row(
            category,
            f"{budget_amount/100:.2f}",
            f"{spent_amount/100:.2f}",
            f"[{status_color}]{remaining_amount/100:.2f}[/{status_color}]",
            f"[{status_color}]{status}[/{status_color}]"
        )
    console.print(table)
