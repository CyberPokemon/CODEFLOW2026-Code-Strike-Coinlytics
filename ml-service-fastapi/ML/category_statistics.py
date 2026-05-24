import pandas as pd
import json
import os

def _prep_amount_columns(df):
    """Helper to ensure Amount is available and clean."""
    if 'Credit' in df.columns and 'Debit' in df.columns:
        df['Credit_Amt'] = pd.to_numeric(df['Credit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
        df['Debit_Amt'] = pd.to_numeric(df['Debit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
    elif 'Amount' in df.columns:
        df['Credit_Amt'] = df.apply(lambda x: x['Amount'] if x['predicted_category'] == 'Income' else 0, axis=1)
        df['Debit_Amt'] = df.apply(lambda x: x['Amount'] if x['predicted_category'] != 'Income' else 0, axis=1)
    else:
        raise ValueError("DataFrame must contain Credit/Debit columns or a unified Amount column.")
    return df

def generate_category_statistics(df):
    """
    Generates detailed statistics for each transaction category.
    Returns statistics grouped by predicted_category with metrics:
    - Total amount
    - Number of transactions
    - Average transaction amount
    - Percentage of total income
    - Percentage of total expenses
    """
    df = _prep_amount_columns(df).copy()
    
    # Calculate totals
    total_income = df['Credit_Amt'].sum()
    total_expenses = df['Debit_Amt'].sum()
    
    # Group by category
    category_stats = []
    
    for category in df['predicted_category'].unique():
        category_df = df[df['predicted_category'] == category]
        
        # Calculate metrics
        credit_amt = category_df['Credit_Amt'].sum()
        debit_amt = category_df['Debit_Amt'].sum()
        transaction_count = len(category_df)
        
        # Net amount (credit - debit)
        net_amount = credit_amt - debit_amt
        
        # Average transaction amount
        avg_amount = net_amount / transaction_count if transaction_count > 0 else 0
        
        # Percentage calculations
        pct_of_income = (credit_amt / total_income * 100) if total_income > 0 else 0
        pct_of_expenses = (debit_amt / total_expenses * 100) if total_expenses > 0 else 0
        
        category_stats.append({
            "category": category,
            "total_credit": round(credit_amt, 2),
            "total_debit": round(debit_amt, 2),
            "net_amount": round(net_amount, 2),
            "transaction_count": transaction_count,
            "average_transaction": round(avg_amount, 2),
            "percentage_of_income": round(pct_of_income, 2),
            "percentage_of_expenses": round(pct_of_expenses, 2)
        })
    
    # Sort by net_amount descending
    category_stats.sort(key=lambda x: x['net_amount'], reverse=True)
    
    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_savings": round(total_income - total_expenses, 2),
        "category_statistics": category_stats
    }

def print_category_statistics(stats):
    """Pretty print category statistics."""
    print("\n" + "="*80)
    print("CATEGORY-WISE FINANCIAL BREAKDOWN")
    print("="*80)
    
    print(f"\nTotal Income: {stats['total_income']:,.2f}")
    print(f"Total Expenses: {stats['total_expenses']:,.2f}")
    print(f"Net Savings: {stats['net_savings']:,.2f}\n")
    
    print(f"{'Category':<20} {'Amount':<15} {'Count':<8} {'Avg Txn':<12} {'% Income':<10} {'% Expense':<10}")
    print("-"*80)
    
    for cat in stats['category_statistics']:
        print(
            f"{cat['category']:<20} "
            f"{cat['net_amount']:>13,.2f}  "
            f"{cat['transaction_count']:>6}  "
            f"{cat['average_transaction']:>10,.2f}  "
            f"{cat['percentage_of_income']:>8.2f}%  "
            f"{cat['percentage_of_expenses']:>8.2f}%"
        )
    
    print("="*80)

def process_and_save_statistics(csv_path, output_json_path="test/category_statistics.json"):
    """
    Load CSV, generate statistics, and save to JSON.
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} transactions from {csv_path}")
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return None
    
    # Generate statistics
    stats = generate_category_statistics(df)
    
    # Print to console
    print_category_statistics(stats)
    
    # Save to JSON
    os.makedirs(os.path.dirname(output_json_path) or "test", exist_ok=True)
    with open(output_json_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"\n✓ Saved category statistics to {output_json_path}")
    
    return stats

if __name__ == "__main__":
    import sys
    
    # Accept file path from command line
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
    else:
        input_csv = "test/final_processed_statement.csv"
    
    if os.path.exists(input_csv):
        process_and_save_statistics(input_csv)
    else:
        print(f"Error: {input_csv} not found. Run runner.py first to generate it.")
