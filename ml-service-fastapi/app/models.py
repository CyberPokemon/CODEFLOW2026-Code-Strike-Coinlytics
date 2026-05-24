from sqlalchemy import Column, BigInteger, String, Float, ForeignKey, Date
from app.database import Base

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, index=True)

    table_id = Column(BigInteger)

    sl_no = Column(BigInteger)

    txn_date = Column(Date)

    particulars = Column(String)

    credit = Column(Float)

    debit = Column(Float)

    balance = Column(Float)

    user_id = Column(BigInteger, ForeignKey("users.id"))
