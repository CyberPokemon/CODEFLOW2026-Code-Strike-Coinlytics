import os

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

CATEGORIES_NORMAL_THRESHOLD = [
    "Food",
    "Travel",
    "Shopping",
    "Bills & Utilities",
    "EMI/Loan",
    "Rent/Housing",
]

CATEGORIES_HIGH_THRESHOLD = [
    "Transfer",
    "Investment",
    "Income",
    "Other",
]


def get_anomaly_threshold_categories():
    return {
        "categories_normal_threshold": CATEGORIES_NORMAL_THRESHOLD,
        "categories_high_threshold": CATEGORIES_HIGH_THRESHOLD,
    }


def _prep_amount_column(df):
    """Ensure Amount is available as a clean numeric column."""
    if "Debit" in df.columns:
        df["Amount"] = pd.to_numeric(df["Debit"].replace({",": ""}, regex=True), errors="coerce").fillna(0)
    elif "Amount" not in df.columns:
        raise ValueError("DataFrame must contain either a 'Debit' or 'Amount' column.")
    return df


def detect_anomalies_iqr(df):
    """Rule-based IQR detection for small datasets (< 300 rows)."""
    df = _prep_amount_column(df)
    df["is_anomaly"] = False
    df["anomaly_reason"] = ""
    df["anomaly_method"] = "Statistical (IQR)"
    df["is_low_confidence"] = False

    for category in CATEGORIES_NORMAL_THRESHOLD:
        cat_data = df[(df["predicted_category"] == category) & (df["Amount"] > 0)]
        if len(cat_data) < 3:
            continue

        q1 = cat_data["Amount"].quantile(0.25)
        q3 = cat_data["Amount"].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + (2.0 * iqr)
        effective_bound = max(upper_bound, 1000)

        anomaly_mask = (df["predicted_category"] == category) & (df["Amount"] > effective_bound)
        df.loc[anomaly_mask, "is_anomaly"] = True

        for idx in df[anomaly_mask].index:
            amt = df.loc[idx, "Amount"]
            df.loc[idx, "anomaly_reason"] = (
                f"{amt:,.2f} is unusually high for {category}. "
                f"Typical spend is < {effective_bound:,.0f}."
            )

    for category in CATEGORIES_HIGH_THRESHOLD:
        cat_data = df[(df["predicted_category"] == category) & (df["Amount"] > 0)]
        if len(cat_data) < 3:
            continue

        q1 = cat_data["Amount"].quantile(0.25)
        q3 = cat_data["Amount"].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + (3.0 * iqr)

        if category == "Income":
            effective_bound = max(upper_bound, 100000)
            reason_template = (
                "Suspicious high income {amt:,.2f}. "
                "Typical income is < {bound:,.0f}. Could be from unknown source."
            )
        elif category == "Other":
            effective_bound = max(upper_bound, 10000)
            reason_template = "Suspicious transaction {amt:,.2f}. Typical is < {bound:,.0f}."
        else:
            effective_bound = max(upper_bound, 50000)
            reason_template = (
                f"{{amt:,.2f}} is an exceptionally large {category}. "
                f"Typical {category.lower()} is < {{bound:,.0f}}."
            )

        anomaly_mask = (df["predicted_category"] == category) & (df["Amount"] > effective_bound)
        df.loc[anomaly_mask, "is_anomaly"] = True

        if category == "Other":
            df.loc[anomaly_mask, "is_low_confidence"] = True

        for idx in df[anomaly_mask].index:
            amt = df.loc[idx, "Amount"]
            df.loc[idx, "anomaly_reason"] = reason_template.format(amt=amt, bound=effective_bound)

    return df


def detect_anomalies_ml(df):
    """Isolation Forest detection for large datasets (> 300 rows)."""
    df = _prep_amount_column(df)
    df["is_anomaly"] = False
    df["anomaly_reason"] = ""
    df["anomaly_method"] = "Machine Learning (Isolation Forest)"

    expense_mask = df["Amount"] > 0
    expense_df = df[expense_mask].copy()

    if len(expense_df) < 10:
        return detect_anomalies_iqr(df)

    features = expense_df[["Amount", "predicted_category"]]
    features_encoded = pd.get_dummies(features, columns=["predicted_category"])

    iso_forest = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    expense_df["if_score"] = iso_forest.fit_predict(features_encoded)

    os.makedirs("model", exist_ok=True)
    anomaly_model_path = os.path.join("model", "anomaly_detector.joblib")
    joblib.dump(
        {
            "model": iso_forest,
            "feature_columns": features_encoded.columns.tolist(),
        },
        anomaly_model_path,
    )
    print(f"Saved anomaly detection model to {anomaly_model_path}")

    anomaly_indices = expense_df[expense_df["if_score"] == -1].index
    df.loc[anomaly_indices, "is_anomaly"] = True

    for idx in anomaly_indices:
        amt = df.loc[idx, "Amount"]
        cat = df.loc[idx, "predicted_category"]

        if cat == "Income":
            reason = f"Suspicious income {amt:,.2f}. ML flagged as unusual pattern (possible unknown source)."
        elif cat == "Other":
            reason = f"Suspicious transaction {amt:,.2f} (low-confidence categorization). ML flagged as irregular."
        else:
            reason = f"ML flagged {amt:,.2f} as a highly irregular pattern for {cat}."

        df.loc[idx, "anomaly_reason"] = reason

    return df
