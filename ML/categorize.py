import pandas as pd
import numpy as np
import re
import os
import joblib
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

####################################################
# 1. CLEANING FUNCTION
####################################################

BANKING_WORDS = {
    "upi",
    "imps",
    "neft",
    "rtgs",
    "txn",
    "txnid",
    "payment",
    "transfer",
    "ref",
    "dr",
    "cr",
    "debit",
    "credit",
    "limited",
    "ltd",
    "india", # Added to prevent the model from learning "india" as a feature
    "nan",   # Added to catch pandas NaN string conversions
    "inb"
}

def clean_text(text):
    # Handle missing/NaN values safely
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # remove numbers
    text = re.sub(r"\d+", " ", text)

    # replace special chars
    text = re.sub(r"[^a-zA-Z ]", " ", text)

    # tokenize
    words = text.split()

    # remove banking words
    words = [w for w in words if w not in BANKING_WORDS]

    return " ".join(words)


####################################################
# 2. SYNTHETIC DATA
####################################################

food_merchants = [
    "swiggy", "zomato", "dominos", "pizza hut", "kfc", "burger king",
    "blinkit", "zepto", "instamart", "mcdonalds", "starbucks", 
    "chaayos", "haldirams", "bigbasket", "eatclub"
]

travel_merchants = [
    "uber", "ola", "irctc", "indrive", "yatrisathi", "rapido", "airindia",
    "makemytrip", "goibibo", "easemytrip", "redbus", "ixigo", "indigo", "spicejet", "akasa"
]

shopping_merchants = [
    "amazon", "flipkart", "myntra", "meesho", "nykaa", "ajio", 
    "tata cliq", "jiomart", "reliance smart", "dmart", "croma", 
    "reliance digital", "max fashion", "pantaloons", "shoppers stop"
]

subscription_merchants = [
    "netflix", "spotify", "amazon prime", "hotstar", "hoichoi",
    "sonyliv", "zee5", "jiocinema", "youtube premium", "apple", 
    "wynk", "kindle"
]

income_merchants = [
    "salary credit", "interest credit", "salary", 
    "dividend", "cashback", "reimbursement", "rent", 
    "pension", "refund", "bonus", "stipend"
]

investment_merchants = [
    "zerodha", "groww", "mutual fund", "upstox", "angel one", 
    "coin", "kuvera", "indmoney", "paytm money", "epfo", 
    "ppf", "sip", "icici direct", "hdfc sec", "sbi mutual fund"
]
####################################################
# DATA AUGMENTATION (WITH NOISE)
####################################################

PATTERNS = [
    "UPI/{}/12345",
    "IMPS/{}/98765",
    "{} LIMITED",
    "{} PAYMENT",
    "UPI PAYMENT {}",
    "{} INDIA",
    "TRANSFER {}",
    "{}",
]

def generate_samples(merchant_list, category):
    rows = []

    for merchant in merchant_list:
        for pattern in PATTERNS:
            # 1. Standard pattern
            standard_narration = pattern.format(merchant)
            rows.append({
                "text": standard_narration,
                "category": category
            })
            
            # 2. Noisy pattern (to help ML catch variations like "pizzahut" or "zomto")
            noisy_merchant = merchant.replace(" ", "").replace("a", "", 1)
            noisy_narration = pattern.format(noisy_merchant)
            rows.append({
                "text": noisy_narration,
                "category": category
            })

    return rows


training_data = []

training_data.extend(generate_samples(food_merchants, "Food"))
training_data.extend(generate_samples(travel_merchants, "Travel"))
training_data.extend(generate_samples(shopping_merchants, "Shopping"))
training_data.extend(generate_samples(subscription_merchants, "Subscription"))
training_data.extend(generate_samples(income_merchants, "Income"))
training_data.extend(generate_samples(investment_merchants, "Investment"))

train_df = pd.DataFrame(training_data)
train_df.to_csv("train/train_wo_cleaning.csv",index=False)

####################################################
# CLEAN TRAINING TEXT
####################################################

train_df["clean_text"] = train_df["text"].apply(clean_text)

# Drop any rows where cleaning resulted in an empty string to prevent bad training data
train_df = train_df[train_df["clean_text"] != ""]
train_df.to_csv("train/train_with_cleaning.csv",index=False)

####################################################
# 3. TRAIN TFIDF + LOGISTIC REGRESSION
####################################################

model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1
            )
        ),
        (
            "clf",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced" # Added to handle unequal merchant counts
            )
        )
    ]
)

model.fit(
    train_df["clean_text"],
    train_df["category"]
)

print("Training completed")

####################################################
# 4. READ TRANSACTION CSV
####################################################

try:
    transactions_df = pd.read_csv("test/transactions.csv")
except FileNotFoundError:
    print("Error: transactions.csv not found. Please ensure the file is in the same directory.")
    exit()

transactions_df["clean_text"] = (
    transactions_df["transaction_statement"]
    .apply(clean_text)
)

####################################################
# 5. PREDICT CATEGORY
####################################################

# We only predict on rows that actually have text left after cleaning
transactions_df["predicted_category"] = model.predict(
    transactions_df["clean_text"]
)

####################################################
# OPTIONAL CONFIDENCE SCORE
####################################################

probs = model.predict_proba(
    transactions_df["clean_text"]
)

transactions_df["confidence"] = probs.max(axis=1)

####################################################
# HANDLE LOW CONFIDENCE & EMPTY STRINGS
####################################################

# Override prediction to "Other" if confidence is low OR if the text was completely stripped
transactions_df.loc[
    (transactions_df["confidence"] < 0.40) | (transactions_df["clean_text"] == ""),
    "predicted_category"
] = "Other"

# Force confidence to 0 for empty strings so reports remain accurate
transactions_df.loc[
    transactions_df["clean_text"] == "", 
    "confidence"
] = 0.0

####################################################
# 6. FINAL OUTPUT DATAFRAME
####################################################

result_df = transactions_df[
    [
        "sl_no",
        "transaction_statement",
        "predicted_category",
        "confidence"
    ]
]

print(result_df.head())

####################################################
# SAVE OUTPUT
####################################################

result_df.to_csv(
    "test/categorized_transactions.csv",
    index=False
)

print("Saved categorized_transactions.csv")

####################################################
# SAVE MODEL
####################################################

# Create model folder if it doesn't exist
model_folder = "model"
if not os.path.exists(model_folder):
    os.makedirs(model_folder)
    print(f"Created {model_folder} folder")

# Save model in joblib format
joblib_path = os.path.join(model_folder, "transaction_categorizer.joblib")
joblib.dump(model, joblib_path)
print(f"Saved model to {joblib_path}")

# Save model in pickle format
pkl_path = os.path.join(model_folder, "transaction_categorizer.pkl")
with open(pkl_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Saved model to {pkl_path}")
