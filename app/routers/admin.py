from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, dependencies

router = APIRouter()

@router.post("/create-teacher", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@router.post("/create-student", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_student(db=db, student=student)
