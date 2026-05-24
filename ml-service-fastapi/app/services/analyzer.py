import pandas as pd

def analyze_transactions(records):

    df = pd.DataFrame(records)

    total_credit = df["credit"].sum()

    total_debit = df["debit"].sum()

    avg_balance = df["balance"].mean()

    return {
        "total_credit": float(total_credit),
        "total_debit": float(total_debit),
        "avg_balance": float(avg_balance),
        "transaction_count": len(df)
    }