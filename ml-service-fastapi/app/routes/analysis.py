from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import TransactionRecord
from app.services.analyzer import analyze_transactions

router = APIRouter()


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
    for record in records:
        data.append({
            "txn_date": getattr(record, "txn_date", None),
            "particulars": record.particulars,
            "credit": record.credit,
            "debit": record.debit,
            "balance": record.balance,
            "user_id": record.user_id,
            "table_id": record.table_id,
            "sl_no": getattr(record, "sl_no", None),
        })

    return analyze_transactions(data)


@router.post("/process-transactions")
def process_transactions(batch: TransactionBatchInput):
    try:
        data = []
        for txn in batch.transactions:
            data.append({
                "table_id": txn.table_id,
                "sl_no": txn.sl_no,
                "txn_date": txn.txn_date,
                "particulars": txn.particulars,
                "credit": txn.credit,
                "debit": txn.debit,
                "balance": txn.balance,
                "user_id": txn.user_id,
            })

        return analyze_transactions(data)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
