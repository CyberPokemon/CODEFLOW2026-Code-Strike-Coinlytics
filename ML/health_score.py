import pandas as pd

def _prep_amount_columns(df):
    """Helper to ensure Amount is available and clean."""
    if 'Credit' in df.columns and 'Debit' in df.columns:
        df['Credit_Amt'] = pd.to_numeric(df['Credit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
        df['Debit_Amt'] = pd.to_numeric(df['Debit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
    elif 'Amount' in df.columns:
        # If there's only an Amount column, we assume 'Income' category = Credit, everything else = Debit
        df['Credit_Amt'] = df.apply(lambda x: x['Amount'] if x['predicted_category'] == 'Income' else 0, axis=1)
        df['Debit_Amt'] = df.apply(lambda x: x['Amount'] if x['predicted_category'] != 'Income' else 0, axis=1)
    else:
        raise ValueError("DataFrame must contain Credit/Debit columns or a unified Amount column.")
    return df

def generate_health_score(df):
    """
    Calculates a deterministic Financial Health Score (0-100) based on strict financial ratios.
    Returns the final score and a list of actionable insights for the UI.
    """
    df = _prep_amount_columns(df).copy()
    
    # 1. Aggregate Totals
    total_income = df['Credit_Amt'].sum()
    
    # If no income is detected, we can't calculate ratios properly.
    if total_income == 0:
        return {
            "score": 0,
            "insights": ["No income detected in this statement. Ratios cannot be calculated."],
            "metrics": {}
        }

    # Aggregate specific expense categories
    category_totals = df.groupby('predicted_category')['Debit_Amt'].sum()
    
    total_expenses = df['Debit_Amt'].sum()
    total_emi = category_totals.get('EMI/Loan', 0)
    total_rent = category_totals.get('Rent/Housing', 0)
    total_utilities = category_totals.get('Bills & Utilities', 0)
    total_investments = category_totals.get('Investment', 0)

    # 2. Calculate Strict Financial Ratios
    # Treat investments as savings rather than expenses for the health check
    adjusted_expenses = total_expenses - total_investments
    
    savings_rate = (total_income - adjusted_expenses) / total_income
    emi_burden = total_emi / total_income
    fixed_costs = (total_emi + total_rent + total_utilities) / total_income

    # 3. Scorecard Logic & Explainability Generation
    score = 0
    insights = []
    
    # --- RULE 1: SAVINGS RATE (Weight: 40 points) ---
    if savings_rate >= 0.20:
        score += 40
        insights.append(f"Excellent savings rate ({(savings_rate*100):.1f}%). You are saving the recommended 20%+ of your income.")
    elif savings_rate >= 0.10:
        score += 25
        insights.append(f"Moderate savings rate ({(savings_rate*100):.1f}%). Try to push this above 20%.")
    elif savings_rate > 0:
        score += 10
        insights.append(f"Low savings rate ({(savings_rate*100):.1f}%). You are barely saving money.")
    else:
        score += 0
        insights.append(f"Negative cash flow! You are spending {(abs(savings_rate)*100):.1f}% more than you earn.")

    # --- RULE 2: EMI BURDEN / DTI (Weight: 30 points) ---
    if emi_burden == 0:
        score += 30
        insights.append("Zero EMI burden. You have excellent debt health.")
    elif emi_burden <= 0.30:
        score += 30
        insights.append(f"Healthy EMI burden ({(emi_burden*100):.1f}%). It is well under the 30% danger threshold.")
    elif emi_burden <= 0.40:
        score += 15
        insights.append(f"High EMI burden ({(emi_burden*100):.1f}%). Approaching dangerous debt levels.")
    else:
        score += 0
        insights.append(f"Critical Debt! ({(emi_burden*100):.1f}%). Over 40% of your income is consumed by debt payments.")

    # --- RULE 3: FIXED COST RATIO (Weight: 30 points) ---
    if fixed_costs <= 0.50:
        score += 30
        insights.append(f"Fixed costs (Rent, EMI, Bills) are well-managed at {(fixed_costs*100):.1f}% of income.")
    elif fixed_costs <= 0.70:
        score += 15
        insights.append(f"High fixed costs ({(fixed_costs*100):.1f}%). You have very little disposable income for daily expenses.")
    else:
        score += 0
        insights.append(f"Unstable fixed costs! ({(fixed_costs*100):.1f}%). Your mandatory living expenses are too high for your salary.")
        
    # --- BONUS: INVESTMENT CHECK ---
    if total_investments > 0:
        insights.append("Bonus: We detected active investments (e.g., Mutual Funds, SIPs), indicating good long-term planning.")

    # 4. Final Output Payload
    return {
        "score": score,
        "insights": insights,
        "metrics": {
            "Total Income": total_income,
            "Total Expenses": total_expenses,
            "Savings Rate": round(savings_rate * 100, 2),
            "EMI Burden": round(emi_burden * 100, 2),
            "Fixed Costs Ratio": round(fixed_costs * 100, 2)
        }
    }


####################################################
# DEMO EXECUTION
####################################################
if __name__ == "__main__":
    
    # Mock data outputted from your categorization model
    data = [
        {"transaction_statement": "Salary", "predicted_category": "Income", "Credit": 100000, "Debit": 0},
        
        {"transaction_statement": "House Rent", "predicted_category": "Rent/Housing", "Credit": 0, "Debit": 25000},
        {"transaction_statement": "Electricity", "predicted_category": "Bills & Utilities", "Credit": 0, "Debit": 3000},
        
        {"transaction_statement": "Bajaj Fin EMI", "predicted_category": "EMI/Loan", "Credit": 0, "Debit": 35000},
        
        {"transaction_statement": "Zerodha Coin", "predicted_category": "Investment", "Credit": 0, "Debit": 10000},
        
        {"transaction_statement": "Swiggy", "predicted_category": "Food", "Credit": 0, "Debit": 5000},
        {"transaction_statement": "Uber", "predicted_category": "Travel", "Credit": 0, "Debit": 3000},
    ]
    
    df = pd.DataFrame(data)
    
    print("Calculating Financial Health Score...\n")
    health_report = generate_health_score(df)
    
    print(f"=====================================")
    print(f" FINAL HEALTH SCORE: {health_report['score']} / 100")
    print(f"=====================================\n")
    
    print("--- WHY YOU GOT THIS SCORE ---")
    for insight in health_report['insights']:
        print(insight)
        
    print("\n--- RAW METRICS ---")
    for key, value in health_report['metrics'].items():
        print(f"{key}: {value}")