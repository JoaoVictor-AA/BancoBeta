from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic.types import conint

class UserOut(BaseModel):
    name: str
    id: int
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    name: str
    password: str
    email: EmailStr


class MakeTransaction(BaseModel):
    sender_id: int
    receiver_id: int
    valor: Decimal


class TransactionOut(BaseModel):
    sender_id: int
    receiver_id: int
    valor: Decimal
    uuid: UUID
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None