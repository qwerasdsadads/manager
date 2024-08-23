from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies
from typing import List
from ..dependencies import get_current_user
router = APIRouter()

@router.get("/classes", response_model=List[schemas.Class])
def get_classes(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_classes_for_teacher(db=db, teacher_id=current_user.id)

@router.post("/create-assignment", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_assignment(db=db, assignment=assignment, teacher_id=current_user.id)
