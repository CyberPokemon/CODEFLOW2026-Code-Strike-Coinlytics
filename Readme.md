# 🪙 Coinlytics

> AI-Powered Bank Statement Analyzer for Indian Banking Transactions

## 👨‍💻 Team Details

### Team Name: **Code Strike**

### Team Members
- **Imon Mallik** — Team Lead
- **Soumi Sahu**
- **Santanu Nanadi**
- **Atrij Roy**

---

# 📌 Problem Statement

This project was developed for the **CodeFlow Hackathon** organized by **STCET** in collaboration with fintech company **Pice**.

### Problem Statement:

Build an AI-powered application that:
- Analyzes Indian bank statements (CSV/PDF)
- Categorizes transactions automatically
- Detects recurring payments
- Identifies financial anomalies
- Generates AI-powered financial health insights
- Provides actionable financial recommendations

---

# 🚀 Project Overview

## What is Coinlytics?

**Coinlytics** is an intelligent financial analytics platform that helps users understand their spending behavior from bank statements securely and efficiently.

Users can upload a bank statement file, and the system automatically:

✅ Categorizes transactions
✅ Detects unusual spending patterns
✅ Generates financial health scores
✅ Provides savings recommendations
✅ Ensures data privacy and security

---

# 🌟 Key Features

## 📂 Smart Statement Upload
- Upload bank statements in CSV format
- Backend securely processes uploaded files
- Data encrypted before storage

## 🧠 AI-Powered Transaction Categorization
Automatically categorizes transactions into:
- Food
- Travel
- Shopping
- Rent
- Bills
- EMI
- Entertainment
- Others

## 🔍 Anomaly Detection
Detects:
- Unusual spending
- Sudden spikes in expenses
- Suspicious transaction behavior

## 📈 Financial Health Score
Generates a financial score between 0-100 based on:
- Savings ratio
- EMI burden
- Fixed expenses
- Spending behavior

## 🔐 Security First Architecture
To maintain user privacy:
- Uploaded files are encrypted
- Database records deleted after **30 minutes of inactivity**
- Server files automatically deleted after **1 hour**

---

# 🏗️ System Architecture

To achieve:
- ⚡ Zero latency
- 🎯 High accuracy
- 🔍 100% explainability

We designed a hybrid AI architecture instead of relying entirely on black-box Large Language Models.

The pipeline contains:

1. Hybrid Transaction Categorizer
2. Dynamic Anomaly Detector
3. Deterministic Financial Scorecard

---

# ⚙️ Core Components

## 1️⃣ Hybrid Categorization Engine

### Files:
- `categorize.py`
- `category_infer.py`

### Objective
Classify noisy bank narratives such as:

```text
UPI/12345/SWIGGY/BLR
NEFT-AMAZONPAY
IMPS-UBER
```

into meaningful categories.

### 🔹 Fast-Path Dictionary Engine
A hardcoded merchant dictionary instantly recognizes common Indian merchants:
- Swiggy
- Zomato
- Amazon
- Uber
- Ola

This provides:
- Ultra-fast execution
- Near-zero latency
- High precision

### 🔹 ML Fallback Pipeline
Unknown transaction descriptions are cleaned and processed through:

- TF-IDF Vectorizer
- Logistic Regression Classifier

### Data Cleaning Includes:
- Removing banking noise
- Removing UPI/NEFT/UTR identifiers
- Text normalization

### Confidence Threshold
If model confidence is below **40%**, the transaction is categorized safely as:

```text
Other
```

This prevents incorrect predictions.

---

# 🧪 Dynamic Anomaly Detection

### File:
- `anomaly_detector.py`

### Objective
Identify irregular or suspicious spending behavior.

To avoid ML cold-start problems, we implemented a dynamic routing system.

## 🔹 Small Dataset Mode (≤ 300 Rows)
Uses:

### Interquartile Range (IQR)
Category-wise statistical boundaries detect mathematical outliers.

Example:
- ₹15,000 Food expense → anomaly
- ₹15,000 Travel expense → possibly normal

### Benefits
- Accurate for short-term statements
- Prevents false positives
- Explainable output

---

## 🔹 Large Dataset Mode (> 300 Rows)
Activates:

### Isolation Forest ML Model

Features include:
- One-Hot Encoded categories
- Context-aware anomaly learning
- Scalable detection

This enables intelligent spending analysis at scale.

---

# 💰 Financial Health Scorecard

### File:
- `health_score.py`

### Objective
Generate a transparent and explainable financial health score.

### Metrics Used

## 🔹 Savings Rate
Target:

```text
> 20%
```

## 🔹 Debt-to-Income Ratio
Danger Zone:

```text
> 40%
```

## 🔹 Fixed Cost Ratio
Calculated using:

```text
(Rent + Bills + EMI) / Income
```

---

## Why Rule-Based Instead of Neural Networks?

Financial systems require:
- Transparency
- Auditability
- Explainability

Our deterministic engine provides actionable insights such as:

> “Your financial score dropped because EMI burden exceeded 40%.”

instead of black-box AI outputs.

---

# 🛡️ Cybersecurity & Privacy

Security was one of the core pillars of Coinlytics.

## Measures Implemented

### 🔐 File Encryption
Uploaded bank statements are encrypted before storage.

### ⏳ Automatic Database Cleanup
Inactive records deleted after:

```text
30 Minutes
```

### 🗑️ Automatic File Removal
Server-side uploaded files deleted after:

```text
1 Hour
```

### 🔒 Minimal Data Retention
No long-term financial data storage.

---

# 🧰 Tech Stack

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Spring Boot
- PostgreSQL

## AI / Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn

---

# 🧠 Three Core Pillars Achieved

## 🌐 Web Development
Responsive frontend and secure backend architecture.

## 🤖 Artificial Intelligence
Hybrid ML pipeline with explainable outputs.

## 🔐 Cybersecurity
Encryption, auto-deletion, and secure data lifecycle.

---

# 📊 Workflow

```text
User Uploads CSV
        ↓
Backend Accepts & Encrypts File
        ↓
Data Stored Securely in PostgreSQL
        ↓
ML Pipeline Processes Transactions
        ↓
Categorization + Anomaly Detection
        ↓
Financial Health Score Generated
        ↓
Insights & Recommendations Displayed
        ↓
Auto Cleanup & File Deletion
```

---

# 🎯 Why Coinlytics Stands Out

✅ Explainable AI

✅ Real-time processing

✅ Hybrid AI + Statistical Intelligence

✅ Security-first architecture

✅ Optimized for Indian banking narratives

✅ Practical fintech use case

---

# 🔮 Future Improvements

- PDF statement support
- OCR integration
- Real-time bank integrations
- Personalized budgeting assistant
- Investment recommendations
- Multi-bank support
- Advanced fraud detection
- Mobile app deployment

---

# 📸 Demo Highlights

- Upload Indian bank statement
- AI categorizes transactions instantly
- Detects anomalies dynamically
- Generates explainable financial insights
- Secure auto-cleanup mechanism

---

# 🏁 Conclusion

Coinlytics combines:

- AI
- Statistical intelligence
- Secure engineering
- Explainable fintech analytics

into a single scalable platform.

Our project demonstrates how practical AI systems can be designed responsibly for real-world fintech applications.

---

# 🙌 Acknowledgements

Special thanks to:

- **STCET** for organizing CodeFlow Hackathon
- **Pice** for the fintech problem statement
- All mentors and organizers

---

# 📬 Contact

### Team Code Strike

For queries or collaboration opportunities:

- Imon Mallik
- Soumi Sahu
- Santanu Nanadi
- Atrij Roy

---

# ⭐ Coinlytics

### “Smart Financial Insights with Explainable AI”

