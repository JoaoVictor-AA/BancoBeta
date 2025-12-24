from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hasher(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"None user was found.")
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == id).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found.")
    return user_info


@router.put("/{id}", response_model=schemas.UserOut)
def modify_user(id: int, updated_user: schemas.CreateUser, db: Session = Depends(get_db)):
    to_modify_user = db.query(models.User).filter(models.User.id == id)
    to_modify_user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return to_modify_user.first()


@router.delete("/{id}", response_model=schemas.UserOut)
def delete_user(id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)