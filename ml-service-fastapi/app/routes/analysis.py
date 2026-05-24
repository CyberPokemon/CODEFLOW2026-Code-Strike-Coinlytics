from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import TransactionRecord
from app.services.analyzer import analyze_transactions

router = APIRouter()

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

