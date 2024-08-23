from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/login")
def login(user_credentials: schemas.LoginSchema, db: Session = Depends(dependencies.get_db)):
    user = crud.authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": "fake_token_for_now", "token_type": "bearer"}

@router.get("/me")
def get_user_info(current_user: schemas.User = Depends(get_current_user)):
    return current_user
