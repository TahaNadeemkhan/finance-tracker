import questionary
from features.transactions import transactions
from features.budgets import budgets
from features.analytics.analytics import display_financial_analytics_menu
from features.smart_assistant.smart_assistant import display_smart_assistant_menu
from features.data_management.data_management import display_data_management_menu

def main():
    """
    Main function to run the CLI application.
    """
    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Add Expense",
                "Add Income",
                "List Transactions",
                "Show Balance",
                "Set Budget",
                "View Budgets",
                "Financial Analytics",
                "Smart Assistant",
                "Data Management",
                "Exit"
            ]
        ).ask()

        if choice == "Add Expense":
            transactions.add_expense()
        elif choice == "Add Income":
            transactions.add_income()
        elif choice == "List Transactions":
            days_str = questionary.text("Enter number of days to filter (e.g., 7), or leave empty for all transactions:").ask()
            days = int(days_str) if days_str else None
            transactions.list_transactions(days)
        elif choice == "Show Balance":
            transactions.get_balance()
        elif choice == "Set Budget":
            budgets.set_budget()
        elif choice == "View Budgets":
            budgets.view_budgets()
        elif choice == "Financial Analytics":
            display_financial_analytics_menu()
        elif choice == "Smart Assistant":
            display_smart_assistant_menu()
        elif choice == "Data Management":
            display_data_management_menu()
        elif choice == "Exit" or choice is None:
            break

if __name__ == "__main__":
    main()
