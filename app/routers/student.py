from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies
from typing import List
from ..dependencies import get_current_user
router = APIRouter()

@router.get("/my-classes", response_model=List[schemas.Class])
def get_my_classes(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_classes_for_student(db=db, student_id=current_user.id)

@router.post("/submit-assignment", response_model=schemas.Submission)
def submit_assignment(submission: schemas.SubmissionCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.submit_assignment(db=db, submission=submission, student_id=current_user.id)
