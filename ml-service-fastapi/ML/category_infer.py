import pandas as pd
import numpy as np
import re
import os
import joblib

####################################################
# 1. HARDCODED DICTIONARY (The Fast-Path)
####################################################
# This dictionary catches known merchants instantly. 
# It overrides the ML model to guarantee 100% accuracy on major brands.

MERCHANT_RULES = {
    # Food & Grocery
    "swiggy": "Food", "zomato": "Food", "dominos": "Food", "kfc": "Food",
    "burger king": "Food", "blinkit": "Food", "zepto": "Food", 
    "instamart": "Food", "mcdonalds": "Food", "starbucks": "Food", 
    "chaayos": "Food", "haldirams": "Food", "bigbasket": "Food", "eatclub": "Food",
    
    # Travel & Commute
    "uber": "Travel", "ola": "Travel", "irctc": "Travel", "rapido": "Travel",
    "makemytrip": "Travel", "redbus": "Travel", "namma yatri": "Travel",
    "indrive": "Travel", "yatrisathi": "Travel", "goibibo": "Travel",
    "easemytrip": "Travel", "ixigo": "Travel", "indigo": "Travel",
    "spicejet": "Travel", "akasa": "Travel", "airindia": "Travel",
    
    # Shopping
    "amazon": "Shopping", "amzn": "Shopping", "flipkart": "Shopping", 
    "myntra": "Shopping", "dmart": "Shopping", "reliance smart": "Shopping",
    "meesho": "Shopping", "nykaa": "Shopping", "ajio": "Shopping", 
    "tata cliq": "Shopping", "jiomart": "Shopping", "croma": "Shopping", 
    "reliance digital": "Shopping", "max fashion": "Shopping", 
    "pantaloons": "Shopping", "shoppers stop": "Shopping",
    
    # Subscriptions
    "netflix": "Subscription", "spotify": "Subscription", "hotstar": "Subscription",
    "prime": "Subscription", "youtube premium": "Subscription", "hoichoi": "Subscription",
    "sonyliv": "Subscription", "zee5": "Subscription", "jiocinema": "Subscription", 
    "apple": "Subscription", "wynk": "Subscription", "kindle": "Subscription",
    
    # Investment
    "zerodha": "Investment", "groww": "Investment", "upstox": "Investment", 
    "sip": "Investment", "mutual fund": "Investment", "angel one": "Investment", 
    "coin": "Investment", "kuvera": "Investment", "indmoney": "Investment", 
    "paytm money": "Investment", "epfo": "Investment", "ppf": "Investment", 
    "icici direct": "Investment", "hdfc sec": "Investment", "sbi mutual fund": "Investment",
    
    # Income
    "salary": "Income", "dividend": "Income", "cashback": "Income", 
    "reimbursement": "Income", "rent": "Income", "pension": "Income", 
    "refund": "Income", "bonus": "Income", "stipend": "Income"
}

####################################################
# 2. PAYMENT TYPE RULES (Extract transaction type)
####################################################

PAYMENT_TYPE_RULES = {
    # Income indicators
    "dep tfr": "Income",           # Deposit Transfer
    "deposit": "Income",
    "credit": "Income",
    "salary": "Income",
    "dividend": "Income",
    "interest": "Income",
    "refund": "Income",
    "cashback": "Income",
    
    # Shopping/Purchase indicators
    "pos": "Shopping",             # Point of Sale
    "purchase": "Shopping",
    "wallet load": "Shopping",
    "wallet": "Shopping",
    
    # Cash/ATM
    "atm wdl": "Other",            # ATM Withdrawal
    "atm cash": "Other",
    "atm": "Other",
    
    # Transfers & Payments
    "wdl tfr": "Other",            # Withdrawal Transfer
    "withdrawal": "Other",
    "neft": "Other",
    "imps": "Other",
    "rtgs": "Other",
    "upi": "Other",
    
    # Fees & Charges
    "amc": "Other",                # Annual Maintenance Charge
    "charge": "Other",
    "fee": "Other",
}

####################################################
# 3. ML CLEANING FUNCTION (Must match training exactly)
####################################################

BANKING_WORDS = {
    "upi", "imps", "neft", "rtgs", "txn", "txnid", "payment", 
    "transfer", "ref", "dr", "cr", "debit", "credit", "limited", 
    "ltd", "india", "nan", "inb"
}

def clean_for_ml(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    words = text.split()
    words = [w for w in words if w not in BANKING_WORDS]
    return " ".join(words)

####################################################
# 4. CORE HYBRID ENGINE
####################################################

def categorize_transaction(narration, model):
    """
    Applies the Hybrid Logic: Dictionary → Payment Type → ML Fallback
    Returns a tuple: (Category, Source, Confidence_Score)
    """
    raw_text = str(narration).lower()
    
    # STEP 1: Fast-path Dictionary Lookup (Merchant Rules)
    for key_phrase, category in MERCHANT_RULES.items():
        if key_phrase in raw_text:
            return category, "Dictionary Rule", 1.00
    
    # STEP 2: Payment Type Detection (High confidence)
    for payment_pattern, category in PAYMENT_TYPE_RULES.items():
        if payment_pattern in raw_text:
            return category, "Payment Type Rule", 0.95
            
    # STEP 3: ML Fallback
    cleaned_text = clean_for_ml(raw_text)
    
    # If cleaning stripped everything
    if not cleaned_text.strip():
        return "Other", "Fallback (Empty String)", 0.00
        
    # Predict using the loaded pipeline
    predicted_category = model.predict([cleaned_text])[0]
    confidence_score = np.max(model.predict_proba([cleaned_text]))
    
    # STEP 4: Confidence Threshold
    if confidence_score < 0.40:
        return "Other", "ML (Low Confidence)", round(confidence_score, 2)
        
    return predicted_category, "ML Model", round(confidence_score, 2)


####################################################
# 5. EXECUTION SCRIPT
####################################################

if __name__ == "__main__":
    
    # 1. Load the trained model
    model_path = "model/transaction_categorizer.joblib"
    try:
        loaded_model = joblib.load(model_path)
        print(f"Successfully loaded model from {model_path}")
    except FileNotFoundError:
        print(f"Error: Could not find {model_path}. Run categorize.py first.")
        exit()

    # 2. Read the test data
    input_csv = "test/transactions.csv"
    try:
        transactions_df = pd.read_csv(input_csv)
        print(f"Loaded {len(transactions_df)} transactions from {input_csv}")
    except FileNotFoundError:
        print(f"Error: {input_csv} not found.")
        exit()

    # Ensure the statement column exists
    if "transaction_statement" not in transactions_df.columns:
        print("Error: Column 'transaction_statement' not found in CSV.")
        exit()

    # 3. Apply the Hybrid Categorization Engine
    print("Categorizing transactions...")
    
    # Apply function returns a Series of tuples
    results = transactions_df["transaction_statement"].apply(
        lambda x: categorize_transaction(x, loaded_model)
    )
    
    # Split the tuples into three new columns
    transactions_df[["predicted_category", "prediction_source", "confidence"]] = pd.DataFrame(
        results.tolist(), index=transactions_df.index
    )

    # 4. Format and save the output
    columns_to_save = [
        col for col in ["sl_no", "transaction_statement", "predicted_category", "prediction_source", "confidence"] 
        if col in transactions_df.columns
    ]
    
    result_df = transactions_df[columns_to_save]
    
    output_csv = "test/hybrid_categorized_transactions.csv"
    
    # Create test folder if it doesn't exist
    if not os.path.exists("test"):
        os.makedirs("test")
        
    result_df.to_csv(output_csv, index=False)
    
    print("\nSample Output:")
    print(result_df.head())
    print(f"\nSaved final results to {output_csv}")