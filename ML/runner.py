import pandas as pd
import joblib
import os

# Import your own categorization function from category_infer.py
# (Ensure category_infer.py is in the same folder and the function is named correctly)
from category_infer import categorize_transaction
from anomaly_detector import detect_anomalies_iqr, detect_anomalies_ml

def process_bank_statement(file_path, model_path="model/transaction_categorizer.joblib"):
    print(f"--- Processing {file_path} ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return
        
    print(f"Total Transactions Loaded: {len(df)}")
    
    # 2. Load Categorization Model
    if not os.path.exists(model_path):
        print(f"Error: Categorization model not found at {model_path}")
        return
        
    cat_model = joblib.load(model_path)
    
    # 3. Categorize Transactions
    print("Running Hybrid Categorization Engine...")
    
    # Assuming your CSV has a column named 'transaction_statement'
    results = df["transaction_statement"].apply(
        lambda x: categorize_transaction(x, cat_model)
    )
    df[["predicted_category", "prediction_source", "confidence"]] = pd.DataFrame(
        results.tolist(), index=df.index
    )
    
    # 4. Route to Anomaly Engine based on dataset size
    print("Routing to Anomaly Detection Engine...")
    
    THRESHOLD = 300
    
    if len(df) > THRESHOLD:
        print(f"Dataset > {THRESHOLD} rows. Activating: Machine Learning (Isolation Forest)")
        df = detect_anomalies_ml(df)
    else:
        print(f"Dataset <= {THRESHOLD} rows. Activating: Statistical Engine (IQR)")
        df = detect_anomalies_iqr(df)
        
    # 5. Extract and print results
    anomalies = df[df['is_anomaly'] == True]
    
    print("\n" + "="*50)
    print(f"ANALYSIS COMPLETE: {len(anomalies)} Anomalies Detected")
    print(f"Method Used: {df['anomaly_method'].iloc[0]}")
    print("="*50)
    
    if not anomalies.empty:
        for _, row in anomalies.iterrows():
            print(f"[{row['predicted_category'].upper()}] {row['transaction_statement']}")
            print(f" -> {row['anomaly_reason']}")
            print("-" * 50)
    else:
        print("No anomalies detected.")
        
    # 6. Save final payload for frontend
    output_path = "test/final_processed_statement.csv"
    os.makedirs("test", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved full enriched dataset to {output_path}")

if __name__ == "__main__":
    import sys
    # Accept file path from command line or FastAPI
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
    else:
        input_csv = "test/transactions.csv"
    
    if input_csv:
        process_bank_statement(input_csv)
    else:
        print("Error: No input CSV path provided")