import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import IsolationForest

def _prep_amount_column(df):
    """Helper to ensure Amount is a clean numeric column."""
    if 'Debit' in df.columns:
        df['Amount'] = pd.to_numeric(df['Debit'].replace({',': ''}, regex=True), errors='coerce').fillna(0)
    elif 'Amount' not in df.columns:
        raise ValueError("DataFrame must contain either a 'Debit' or 'Amount' column.")
    return df

def detect_anomalies_iqr(df):
    """Rule-based IQR detection for small datasets (< 300 rows)."""
    df = _prep_amount_column(df)
    df['is_anomaly'] = False
    df['anomaly_reason'] = ""
    df['anomaly_method'] = "Statistical (IQR)"

    categories_to_ignore = ['Income', 'Other', 'Transfer', 'Investment']

    for category in df['predicted_category'].unique():
        if category in categories_to_ignore:
            continue

        cat_data = df[(df['predicted_category'] == category) & (df['Amount'] > 0)]
        if len(cat_data) < 3:
            continue

        Q1 = cat_data['Amount'].quantile(0.25)
        Q3 = cat_data['Amount'].quantile(0.75)
        IQR = Q3 - Q1
        
        upper_bound = Q3 + (2.0 * IQR)
        effective_bound = max(upper_bound, 1000) # Heuristic safeguard

        anomaly_mask = (df['predicted_category'] == category) & (df['Amount'] > effective_bound)
        df.loc[anomaly_mask, 'is_anomaly'] = True
        
        for idx in df[anomaly_mask].index:
            amt = df.loc[idx, 'Amount']
            df.loc[idx, 'anomaly_reason'] = (f"₹{amt:,.2f} is unusually high for {category}. "
                                             f"Typical spend is under ₹{effective_bound:,.0f}.")
    return df

def detect_anomalies_ml(df):
    """Isolation Forest detection for large datasets (> 300 rows)."""
    df = _prep_amount_column(df)
    df['is_anomaly'] = False
    df['anomaly_reason'] = ""
    df['anomaly_method'] = "Machine Learning (Isolation Forest)"

    categories_to_ignore = ['Income', 'Other', 'Transfer', 'Investment']
    
    # Isolate only the expense rows for the ML model
    expense_mask = (~df['predicted_category'].isin(categories_to_ignore)) & (df['Amount'] > 0)
    expense_df = df[expense_mask].copy()

    # If somehow we have no expenses, just return
    if len(expense_df) < 10:
        return detect_anomalies_iqr(df) # Fallback to IQR if expenses are too few

    # Feature Engineering: One-Hot Encode categories + Amount
    # This allows the tree to branch based on category types
    features = expense_df[['Amount', 'predicted_category']]
    features_encoded = pd.get_dummies(features, columns=['predicted_category'])

    # Initialize and fit Isolation Forest
    # contamination=0.02 means we assume roughly 2% of transactions are anomalies
    iso_forest = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    
    # Predict (-1 is anomaly, 1 is normal)
    expense_df['if_score'] = iso_forest.fit_predict(features_encoded)

    # Save the fitted anomaly model and its feature columns for later reuse.
    os.makedirs("model", exist_ok=True)
    anomaly_model_path = os.path.join("model", "anomaly_detector.joblib")
    joblib.dump(
        {
            "model": iso_forest,
            "feature_columns": features_encoded.columns.tolist(),
            "categories_to_ignore": categories_to_ignore,
        },
        anomaly_model_path,
    )
    print(f"Saved anomaly detection model to {anomaly_model_path}")
    
    # Map back to main dataframe
    anomaly_indices = expense_df[expense_df['if_score'] == -1].index
    df.loc[anomaly_indices, 'is_anomaly'] = True
    
    for idx in anomaly_indices:
        amt = df.loc[idx, 'Amount']
        cat = df.loc[idx, 'predicted_category']
        df.loc[idx, 'anomaly_reason'] = f"ML flagged ₹{amt:,.2f} as a highly irregular pattern for {cat}."

    return df

