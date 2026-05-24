import pandas as pd
import joblib
import os

# Import categorization and anomaly detection functions
from category_infer import categorize_transaction
from anomaly_detector import detect_anomalies_iqr, detect_anomalies_ml
from health_score import generate_health_score
from category_statistics import generate_category_statistics, print_category_statistics

def categorize_all_transactions(df, model):
    """
    STEP 1: Categorize all transactions using category_infer.py
    """
    print("\n" + "="*50)
    print("STEP 1: TRANSACTION CATEGORIZATION")
    print("="*50)
    print("Running Hybrid Categorization Engine (Dictionary + ML)...")
    
    # Determine the transaction description column
    # Support multiple column name variations from different banks/formats
    possible_columns = [
        "transaction_statement",
        "Details",
        "description",
        "Description",
        "about",
        "About",
        "Remarks",
        "remarks",
        "Notes",
        "notes",
        "Transaction",
        "transaction",
        "Memo",
        "memo",
        "Narrative",
        "narrative"
    ]
    
    statement_col = None
    for col in possible_columns:
        if col in df.columns:
            statement_col = col
            break
    
    if statement_col is None:
        print(f"Error: Could not find transaction description column")
        print(f"Available columns: {list(df.columns)}")
        print(f"Expected one of: {possible_columns}")
        return df
    
    # Rename the column to transaction_statement for consistency
    if statement_col != "transaction_statement":
        df = df.rename(columns={statement_col: "transaction_statement"})
    
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
    
    # STEP 2: GENERATE CATEGORY STATISTICS
    print("\n" + "="*50)
    print("STEP 2: CATEGORY STATISTICS")
    print("="*50)
    category_stats = generate_category_statistics(df)
    print_category_statistics(category_stats)
    
    # STEP 3: DETECT ANOMALIES
    df = detect_anomalies(df)
    
    # STEP 4: GENERATE FINANCIAL HEALTH SCORE
    print("\n" + "="*50)
    print("STEP 4: FINANCIAL HEALTH ANALYSIS")
    print("="*50)
    health_report = generate_health_score(df)
    
    # STEP 5: EXTRACT AND PRINT RESULTS
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
    
    # --- HEALTH SCORE SUMMARY ---
    print("\n" + "="*50)
    print(f" FINANCIAL HEALTH SCORE: {health_report['score']} / 100")
    print("="*50)
    print("\nKey Insights:")
    for insight in health_report['insights']:
        print(f"  {insight}")
    
    print("\nFinancial Metrics:")
    for key, value in health_report['metrics'].items():
        print(f"  {key}: {value}")
        
    # STEP 6: SAVE RESULTS
    output_path = "test/final_processed_statement.csv"
    os.makedirs("test", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved enriched dataset to {output_path}")
    
    # Save health report as JSON
    import json
    health_report_path = "test/health_report.json"
    with open(health_report_path, 'w') as f:
        json.dump(health_report, f, indent=2)
    print(f"✓ Saved health report to {health_report_path}")
    
    # Save category statistics as JSON
    category_stats_path = "test/category_statistics.json"
    with open(category_stats_path, 'w') as f:
        json.dump(category_stats, f, indent=2)
    print(f"✓ Saved category statistics to {category_stats_path}")
    
    # STEP 7: CREATE COMPREHENSIVE RESULTS JSON (Execution Order: Categorize → Statistics → Anomaly → Health)
    results_json = {
        "type_1_transactions": [],
        "type_2_category_statistics": {},
        "type_3_anomalies": [],
        "type_4_health_score": {}
    }
    
    # Type 1: Transaction Classifications
    for _, row in df.iterrows():
        results_json["type_1_transactions"].append({
            "transaction_statement": row["transaction_statement"],
            "predicted_category": row["predicted_category"],
            "confidence": row["confidence"],
            "prediction_source": row["prediction_source"]
        })
    
    # Type 2: Category Statistics
    results_json["type_2_category_statistics"] = category_stats
    
    # Type 3: Anomalies with Reasons
    for _, row in anomalies.iterrows():
        results_json["type_3_anomalies"].append({
            "transaction_statement": row["transaction_statement"],
            "predicted_category": row["predicted_category"],
            "anomaly_reason": row["anomaly_reason"],
            "confidence": row["confidence"]
        })
    
    # Type 4: Health Score
    results_json["type_4_health_score"] = {
        "score": health_report["score"],
        "insights": health_report["insights"],
        "metrics": health_report["metrics"]
    }
    
    # Save comprehensive results
    results_path = "test/analysis_results.json"
    with open(results_path, 'w') as f:
        json.dump(results_json, f, indent=2)
    print(f"✓ Saved comprehensive results to {results_path}")

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