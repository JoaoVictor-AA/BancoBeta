from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.types import conint

class UserOut(BaseModel):
    name: str
    id: int


class CreateUser(BaseModel):
    name: str
    password: str
    email: str


class MakeTransaction(BaseModel):
    sender_id: int
    receiver_id: int
    valor: float


class TransactionOut(BaseModel):
    sender_id: int
    receiver_id: int
    valor: float
    uuid: UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None