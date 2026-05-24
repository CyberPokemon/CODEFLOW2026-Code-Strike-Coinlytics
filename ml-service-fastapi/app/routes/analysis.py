from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.database import SessionLocal
from app.models import TransactionRecord
from app.services.analyzer import analyze_transactions
import pandas as pd
import os
import subprocess
import sys

router = APIRouter()

# Pydantic models for request/response
class TransactionInput(BaseModel):
    table_id: int
    sl_no: Optional[int] = None
    txn_date: Optional[date] = None
    particulars: str
    credit: Optional[float] = 0.0
    debit: Optional[float] = 0.0
    balance: Optional[float] = 0.0
    user_id: int

class TransactionBatchInput(BaseModel):
    transactions: List[TransactionInput]

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/analyze/{user_id}/{table_id}")
def analyze(user_id: int, table_id: int, db: Session = Depends(get_db)):

    records = db.query(TransactionRecord)\
        .filter(
            TransactionRecord.user_id == user_id,
            TransactionRecord.table_id == table_id
        ).all()

    if not records:
        return {
            "message": "No transactions found"
        }

    data = []

    for r in records:
        data.append({
            "credit": r.credit,
            "debit": r.debit,
            "balance": r.balance,
            "particulars": r.particulars
        })

    result = analyze_transactions(data)

    return result

@router.post("/process-transactions")
def process_transactions(batch: TransactionBatchInput):
    """
    Accept transaction data, save to CSV, and run ML analysis pipeline
    """
    try:
        # 1. Create infer directory if it doesn't exist
        infer_dir = "infer"
        os.makedirs(infer_dir, exist_ok=True)
        
        # 2. Convert transaction data to DataFrame
        df_data = []
        for txn in batch.transactions:
            df_data.append({
                "table_id": txn.table_id,
                "sl_no": txn.sl_no,
                "txn_date": txn.txn_date,
                "particulars": txn.particulars,
                "credit": txn.credit,
                "debit": txn.debit,
                "balance": txn.balance,
                "user_id": txn.user_id,
                "transaction_statement": txn.particulars  # For runner.py compatibility
            })
        
        df = pd.DataFrame(df_data)
        
        # 3. Save to CSV
        csv_path = os.path.join(infer_dir, "transactions.csv")
        df.to_csv(csv_path, index=False)
        
        print(f"✓ Saved {len(batch.transactions)} transactions to {csv_path}")
        
        # 4. Run runner.py pipeline
        ml_dir = os.path.dirname(os.path.abspath(__file__))
        runner_path = os.path.join(ml_dir, "../../..", "ML", "runner.py")
        
        result = subprocess.run(
            [sys.executable, runner_path, csv_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(runner_path)
        )
        
        print(f"✓ Runner completed with return code: {result.returncode}")
        
        return {
            "status": "success",
            "message": f"Processed {len(batch.transactions)} transactions",
            "csv_path": csv_path,
            "output_file": os.path.join(infer_dir, "final_processed_statement.csv"),
            "runner_output": result.stdout,
            "runner_errors": result.stderr if result.stderr else None
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

