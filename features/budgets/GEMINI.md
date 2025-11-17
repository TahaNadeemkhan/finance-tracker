# Day 3: Budget Management

## Goal
Implement category-based budgeting to help users manage their spending.

## Learning Focus
- File operations for reading and writing budget data.
- Integrating with transaction data for spending tracking.
- Displaying financial summaries using Rich.

## Fintech Concepts
- **Budget**: A plan for how to spend and save money.
- **Category-based budgeting**: Allocating specific amounts of money to different spending categories.
- **Budget alerts**: Notifying users when they are approaching or have exceeded their budget.

## Features to Build

### 1. Set Budget
Flow:
1. Ask for category (use existing expense categories from transactions).
2. Ask for budget amount (validate: must be a positive number).
3. Save to `budgets.txt` (format: `category,amount_paisa`).

### 2. View Budgets
Display:
- Show all set budgets in a Rich table.
- For each budget, calculate:
    - Total spent in that category (from `transactions.txt`).
    - Remaining amount.
    - Status (e.g., "Under Budget", "Over Budget").
- Columns: Category, Budget Amount, Spent Amount, Remaining Amount, Status.
- Color: Green for under budget, Red for over budget.

## Success Criteria

✅ Can set budgets for different categories with validation.
✅ Can view all set budgets.
✅ Accurately calculates spent and remaining amounts for each budget.
✅ Clearly indicates budget status (under/over) with appropriate coloring.
✅ Money calculations are accurate (no float errors).