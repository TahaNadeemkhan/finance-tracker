import questionary
from rich.console import Console
from rich.panel import Panel
from features.transactions.transactions import load_transactions
from datetime import datetime, timedelta

console = Console()

def get_personalized_advice():
    """
    Generates personalized financial advice based on the user's recent financial activity.
    """
    console.print(Panel("[bold yellow]Smart Financial Assistant[/bold yellow]", expand=False))
    console.print("Connecting to the Smart Assistant for personalized advice...")

    # 1. Gather financial summary
    transactions = load_transactions()
    if not transactions:
        console.print("[bold red]No transactions found. Cannot generate advice.[/bold red]")
        return

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    recent_transactions = [
        t for t in transactions 
        if start_date <= t["date"] <= end_date
    ]

    total_income = sum(t["amount"] for t in recent_transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in recent_transactions if t["type"] == "expense")

    spending_by_category = {}
    for t in recent_transactions:
        if t["type"] == "expense":
            spending_by_category[t["category"]] = spending_by_category.get(t["category"], 0) + t["amount"]

    # 2. Format the prompt for the LLM
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

    # 3. Get advice from the LLM (simulated for now)
    # In a real application, you would make an API call to an LLM here.
    # For this example, we'll use a hardcoded response.
    simulated_llm_response = """
1.  **Review Your Food Spending:** Your spending on food seems quite high at nearly 40% of your expenses. Look for opportunities to cook at home more often or find less expensive dining options.
2.  **Create a Shopping Budget:** Your shopping expenses are also significant. Consider setting a specific budget for shopping each month to keep this category in check.
3.  **Increase Your Savings:** With your current income and expenses, you have an opportunity to save more. Try to set a savings goal for each month, even if it's a small amount to start.
4.  **Track Your Bills:** Make sure you are paying all your bills on time to avoid late fees. You might be able to negotiate lower rates with some of your service providers.
"""

    # 4. Display the advice
    console.print(Panel(simulated_llm_response, title="[bold green]Personalized Recommendations[/bold green]", expand=False))

def display_smart_assistant_menu():
    """
    Displays the smart assistant menu and handles user choices.
    """
    choice = questionary.select(
        "Smart Assistant Menu:",
        choices=[
            "Get Personalized Advice",
            "Back to Main Menu"
        ]
    ).ask()

    if choice == "Get Personalized Advice":
        get_personalized_advice()
    elif choice == "Back to Main Menu":
        return
