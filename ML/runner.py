import pandas as pd
import joblib
import os

# Import categorization and anomaly detection functions
from category_infer import categorize_transaction
from anomaly_detector import detect_anomalies_iqr, detect_anomalies_ml

def categorize_all_transactions(df, model):
    """
    STEP 1: Categorize all transactions using category_infer.py
    """
    print("\n" + "="*50)
    print("STEP 1: TRANSACTION CATEGORIZATION")
    print("="*50)
    print("Running Hybrid Categorization Engine (Dictionary + ML)...")
    
    # Determine the transaction description column
    # Support both 'transaction_statement' and 'Details' (from bank CSVs)
    statement_col = None
    if "transaction_statement" in df.columns:
        statement_col = "transaction_statement"
    elif "Details" in df.columns:
        statement_col = "Details"
        # Create transaction_statement alias for consistency
        df["transaction_statement"] = df["Details"]
    else:
        print(f"Error: Could not find transaction description column")
        print(f"Available columns: {list(df.columns)}")
        return df
    
    # Apply categorization
    results = df["transaction_statement"].apply(
        lambda x: categorize_transaction(x, model)
    )
    
    # Extract category, source, and confidence
    df[["predicted_category", "prediction_source", "confidence"]] = pd.DataFrame(
        results.tolist(), index=df.index
    )
    
    print(f"✓ Categorized {len(df)} transactions")
    print("\nCategory Distribution:")
    print(df["predicted_category"].value_counts())
    
    return df

def detect_anomalies(df):
    """
    STEP 2: Detect anomalies using categorized transactions
    """
    print("\n" + "="*50)
    print("STEP 2: ANOMALY DETECTION")
    print("="*50)
    print("Routing to Anomaly Detection Engine...")
    
    THRESHOLD = 300
    
    if len(df) > THRESHOLD:
        print(f"Dataset > {THRESHOLD} rows → Using ML Engine (Isolation Forest)")
        df = detect_anomalies_ml(df)
    else:
        print(f"Dataset <= {THRESHOLD} rows → Using Statistical Engine (IQR)")
        df = detect_anomalies_iqr(df)
    
    return df

def process_bank_statement(file_path, model_path="model/transaction_categorizer.joblib"):
    print(f"\n{'='*50}")
    print(f"Processing: {file_path}")
    print(f"{'='*50}")
    
    # LOAD DATA
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return
        
    print(f"Total Transactions Loaded: {len(df)}")
    
    # LOAD MODEL
    if not os.path.exists(model_path):
        print(f"Error: Categorization model not found at {model_path}")
        return
        
    cat_model = joblib.load(model_path)
    
    # STEP 1: CATEGORIZE TRANSACTIONS
    df = categorize_all_transactions(df, cat_model)
    
    # STEP 2: DETECT ANOMALIES
    df = detect_anomalies(df)
    
    # STEP 3: EXTRACT AND PRINT RESULTS
    anomalies = df[df['is_anomaly'] == True]
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print(f"Anomalies Detected: {len(anomalies)}")
    print(f"Detection Method: {df['anomaly_method'].iloc[0]}")
    print("="*50)
    
    if not anomalies.empty:
        print("\nFlagged Transactions:")
        for _, row in anomalies.iterrows():
            print(f"\n[{row['predicted_category'].upper()}] {row['transaction_statement']}")
            print(f"  Category Source: {row['prediction_source']} (Confidence: {row['confidence']})")
            print(f"  Anomaly Reason: {row['anomaly_reason']}")
    else:
        print("\n✓ No anomalies detected.")
        
    # STEP 4: SAVE RESULTS
    output_path = "test/final_processed_statement.csv"
    os.makedirs("test", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved enriched dataset to {output_path}")

if __name__ == "__main__":
    import sys
    # Accept file path from command line or FastAPI
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
    else:
        input_csv = "test/trans2.csv"
    
    if input_csv:
        process_bank_statement(input_csv)
    else:
        print("Error: No input CSV path provided")