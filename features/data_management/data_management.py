import questionary
from rich.console import Console
from rich.panel import Panel
import os
import csv
import json
from features.transactions.transactions import load_transactions, TRANSACTIONS_FILE
from features.budgets.budgets import load_budgets, BUDGETS_FILE

console = Console()
EXPORT_DIR = "exports"

def export_data():
    """
    Exports transaction and budget data to a chosen format (CSV or JSON).
    """
    console.print(Panel("[bold blue]Export Data[/bold blue]", expand=False))
    
    export_format = questionary.select(
        "Choose an export format:",
        choices=["CSV", "JSON"]
    ).ask()

    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    transactions = load_transactions()
    budgets = load_budgets()

    if export_format == "CSV":
        export_path = os.path.join(EXPORT_DIR, "export.csv")
        try:
            with open(export_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["type", "date", "category", "description", "amount"])
                for t in transactions:
                    writer.writerow(["transaction", t["date"].strftime("%Y-%m-%d"), t["category"], t["description"], t["amount"]])
                for category, amount in budgets.items():
                    writer.writerow(["budget", "", category, "", amount])
            console.print(f"[bold green]Data successfully exported to {export_path}[/bold green]")
        except IOError as e:
            console.print(f"[bold red]Error exporting data to CSV: {e}[/bold red]")

    elif export_format == "JSON":
        export_path = os.path.join(EXPORT_DIR, "export.json")
        data_to_export = {
            "transactions": [
                {
                    "date": t["date"].strftime("%Y-%m-%d"),
                    "type": t["type"],
                    "category": t["category"],
                    "description": t["description"],
                    "amount": t["amount"]
                } for t in transactions
            ],
            "budgets": budgets
        }
        try:
            with open(export_path, "w") as f:
                json.dump(data_to_export, f, indent=4)
            console.print(f"[bold green]Data successfully exported to {export_path}[/bold green]")
        except IOError as e:
            console.print(f"[bold red]Error exporting data to JSON: {e}[/bold red]")

def import_data():
    """
    Imports transaction and budget data from a chosen file (CSV or JSON).
    """
    console.print(Panel("[bold blue]Import Data[/bold blue]", expand=False))
    
    import_path = questionary.text("Enter the path to the import file:").ask()

    if not os.path.exists(import_path):
        console.print("[bold red]File not found. Please provide a valid path.[/bold red]")
        return

    file_extension = os.path.splitext(import_path)[1].lower()

    try:
        if file_extension == ".csv":
            with open(import_path, "r") as f:
                reader = csv.reader(f)
                next(reader) # Skip header
                
                transactions_to_add = []
                budgets_to_add = {}

                for row in reader:
                    item_type, date, category, description, amount = row
                    if item_type == "transaction":
                        transactions_to_add.append(f"{date},{'expense' if float(amount) < 0 else 'income'},{category},{description},{int(float(amount))}")
                    elif item_type == "budget":
                        budgets_to_add[category] = int(float(amount))
                
                with open(TRANSACTIONS_FILE, "a") as f:
                    for t in transactions_to_add:
                        f.write(t + "\n")
                
                existing_budgets = load_budgets()
                existing_budgets.update(budgets_to_add)
                with open(BUDGETS_FILE, "w") as f:
                    for cat, amt in existing_budgets.items():
                        f.write(f"{cat},{amt}\n")
                
                console.print(f"[bold green]Successfully imported {len(transactions_to_add)} transactions and {len(budgets_to_add)} budgets from CSV.[/bold green]")

        elif file_extension == ".json":
            with open(import_path, "r") as f:
                data_to_import = json.load(f)
            
            transactions_to_add = data_to_import.get("transactions", [])
            budgets_to_add = data_to_import.get("budgets", {})

            with open(TRANSACTIONS_FILE, "a") as f:
                for t in transactions_to_add:
                    f.write(f"{t['date']},{t['type']},{t['category']},{t['description']},{t['amount']}\n")
            
            existing_budgets = load_budgets()
            existing_budgets.update(budgets_to_add)
            with open(BUDGETS_FILE, "w") as f:
                for cat, amt in existing_budgets.items():
                    f.write(f"{cat},{amt}\n")

            console.print(f"[bold green]Successfully imported {len(transactions_to_add)} transactions and {len(budgets_to_add)} budgets from JSON.[/bold green]")

        else:
            console.print("[bold red]Unsupported file format. Please use .csv or .json files.[/bold red]")

    except Exception as e:
        console.print(f"[bold red]An error occurred during import: {e}[/bold red]")


def display_data_management_menu():
    """
    Displays the data management menu and handles user choices.
    """
    choice = questionary.select(
        "Data Management Menu:",
        choices=[
            "Export Data",
            "Import Data",
            "Back to Main Menu"
        ]
    ).ask()

    if choice == "Export Data":
        export_data()
    elif choice == "Import Data":
        import_data()
    elif choice == "Back to Main Menu":
        return
