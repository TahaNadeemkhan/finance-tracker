# Day 5: Smart Financial Assistant

## Today's Goal
Integrate an AI-powered smart assistant to provide personalized financial advice and insights.

## Learning Focus
- Interacting with a Large Language Model (LLM) for generating insights.
- Crafting effective prompts for financial advice.
- Presenting AI-generated content in a user-friendly way.

## Fintech Concepts
- **Robo-advisors**: Automated, algorithm-driven financial planning services.
- **Personalized Finance**: Tailoring financial advice to an individual's specific situation.
- **Natural Language Insights**: Presenting data-driven insights in a conversational, easy-to-understand format.

## Features to Build

### 1. Get Personalized Advice
- **Flow**:
    1. The user selects "Get Personalized Advice" from the main menu.
    2. The application gathers a summary of the user's recent financial activity (e.g., total income, total expenses, spending by category for the last 30 days).
    3. This summary is formatted into a prompt for a Large Language Model (LLM).
    4. The application sends the prompt to the LLM and gets a response.
    5. The LLM's response (the personalized advice) is displayed to the user in a clean, readable format (e.g., using Rich's Panel).

- **Prompt Example**:
  ```
  "As a friendly financial assistant, analyze the following financial summary and provide 3-5 actionable, personalized recommendations. The user is trying to improve their financial health.

  **Financial Summary (Last 30 Days):**
  - **Total Income:** $2500
  - **Total Expenses:** $2100
  - **Spending by Category:**
    - Food: $800 (38%)
    - Shopping: $600 (29%)
    - Transport: $300 (14%)
    - Bills: $400 (19%)

  **Your Recommendations:**"
  ```

### 2. Weekly Financial Summary
- **Flow**:
    1. At the start of each week, the application automatically generates a summary of the previous week's financial activity.
    2. This summary is presented to the user when they first open the app for the week.
    3. The summary should be concise and highlight key trends (e.g., "Your spending was 15% higher than the previous week.").

## Success Criteria
✅ A new "Smart Assistant" option is available in the main menu.
✅ The application can generate a financial summary and use it to get advice from an LLM.
✅ The advice from the LLM is displayed to the user.
✅ The advice is relevant and personalized to the user's financial data.
✅ The output is well-formatted and easy to read.
