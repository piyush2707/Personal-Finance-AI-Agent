import pandas as pd

def process_statement(file):
    # CSV file ko read karna
    df = pd.read_csv(file)
    
    # Basic cleaning (Adjust column names based on your CSV)
    # Hum assume kar rahe hain ki CSV mein 'Date', 'Description', aur 'Amount' columns hain
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'])
    
    # Spending Insights nikalna
    total_spent = df[df['Amount'] > 0]['Amount'].sum()
    total_income = abs(df[df['Amount'] < 0]['Amount'].sum())
    
    # Sabse zyada kharcha kahan hua (Top 5 transactions)
    top_expenses = df.sort_values(by='Amount', ascending=False).head(5)
    
    summary = {
        "total_spent": total_spent,
        "total_income": total_income,
        "balance": total_income - total_spent,
        "top_expenses": top_expenses.to_dict(orient='records')
    }
    
    return df, summary

def get_ai_prompt(summary):
    # Yeh function AI ke liye ek message (prompt) taiyar karega
    prompt = f"""
    You are a professional Financial Advisor. Analyze this spending summary:
    - Total Spent: ${summary['total_spent']}
    - Total Income: ${summary['total_income']}
    - Current Balance: ${summary['balance']}
    - Top 5 Expenses: {summary['top_expenses']}
    
    Please provide:
    1. A brief analysis of the spending habits.
    2. Three actionable tips to save more money next month.
    3. Any red flags in the top expenses.
    """
    return prompt
    
