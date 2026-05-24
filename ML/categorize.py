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
    "upi", "imps", "neft", "rtgs", "txn", "txnid", "payment", 
    "transfer", "ref", "dr", "cr", "debit", "credit", "limited", 
    "ltd", "india", "nan", "inb"
}

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    
    words = text.split()
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

# Create train directory if it doesn't exist
os.makedirs("train", exist_ok=True)

train_df.to_csv("train/train_wo_cleaning.csv", index=False)
print("Saved raw training data to train/train_wo_cleaning.csv")

####################################################
# CLEAN TRAINING TEXT
####################################################

train_df["clean_text"] = train_df["text"].apply(clean_text)

# Drop any rows where cleaning resulted in an empty string to prevent bad training data
train_df = train_df[train_df["clean_text"] != ""]
train_df.to_csv("train/train_with_cleaning.csv", index=False)
print("Saved cleaned training data to train/train_with_cleaning.csv")

####################################################
# 3. TRAIN TFIDF + LOGISTIC REGRESSION
####################################################

print("Starting model training...")

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
                class_weight="balanced"
            )
        )
    ]
)

model.fit(
    train_df["clean_text"],
    train_df["category"]
)

print("Training completed successfully.")

####################################################
# 4. SAVE MODEL
####################################################

# Create model folder if it doesn't exist
model_folder = "model"
os.makedirs(model_folder, exist_ok=True)

# Save model in joblib format
joblib_path = os.path.join(model_folder, "transaction_categorizer.joblib")
joblib.dump(model, joblib_path)
print(f"Saved model to {joblib_path}")

# Save model in pickle format
pkl_path = os.path.join(model_folder, "transaction_categorizer.pkl")
with open(pkl_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Saved model to {pkl_path}")