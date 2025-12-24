from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app import models, schemas, oauth2
from ..database import get_db
from uuid import UUID
from datetime import date, timedelta
router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=schemas.TransactionOut)
def make_transaction(transfer: schemas.MakeTransaction, db: Session = Depends(get_db)):
    new_transaction = models.Transaction(**transfer.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.get("/{uuid}", response_model=schemas.TransactionOut)
def get_by_uuid(uuid_input: UUID, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.uuid == uuid_input).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found any transaction with identifier {uuid_input}")
    return transaction


@router.get("/")
def get_transactions(sender_id_input: int | None= None, receiver_id_input: int | None=None, begin_time: date | None=None, end_time: date | None=None, db: Session = Depends(get_db)):
    query = db.query(models.Transaction)
    if sender_id_input is not None:
        query = query.filter(models.Transaction.sender_id == sender_id_input)
    if receiver_id_input is not None:
        query = query.filter(models.Transaction.receiver_id == receiver_id_input)
    if begin_time:
        query = query.filter(models.Transaction.time >= begin_time)
    if end_time:
        end_time = end_time + timedelta(days=1)
        query = query.filter(models.Transaction.time <= end_time)
    transactions = query.all()
    return transactions