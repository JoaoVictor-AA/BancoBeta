from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/")
def login():
    return {"message": "Login Novo"}