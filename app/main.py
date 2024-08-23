from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, dependencies
from typing import List

from .database import engine, Base

print("你好")
# 创建所有表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 创建数据库表
@app.on_event("startup")
async def startup():
    # 你可以在这里添加初始化数据库的代码
    pass

# 健康检查路由
@app.get("/health")
def read_health():
    return {"status": "Healthy"}

# 登录接口
@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.Login, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user_by_username(db, credentials.username)
    if user is None or not dependencies.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = dependencies.create_jwt_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}

# 获取当前用户信息
@app.get("/users/me", response_model=schemas.User)
def read_current_user(current_user: schemas.User = Depends(dependencies.get_current_user)):
    return current_user

# 校长相关路由
@app.post("/admin/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    # 只有校长可以创建用户
    crud.create_user(db, user)
    return user

@app.get("/admin/users", response_model=List[schemas.User])
def list_users(db: Session = Depends(dependencies.get_db)):
    return crud.get_users(db)

@app.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    crud.delete_user(db, user_id)

# 老师相关路由
@app.post("/teacher/classes", response_model=schemas.Class)
def create_class(class_: schemas.ClassCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_teacher_user)):
    # 只有老师可以创建班级
    return crud.create_class(db, class_)

@app.get("/teacher/classes", response_model=List[schemas.Class])
def list_classes(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_teacher_user)):
    return crud.get_classes(db, current_user.id)

@app.post("/teacher/assignments", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_teacher_user)):
    # 只有老师可以创建作业
    return crud.create_assignment(db, assignment)

@app.get("/teacher/assignments", response_model=List[schemas.Assignment])
def list_assignments(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_teacher_user)):
    return crud.get_assignments(db, current_user.id)

# 学生相关路由
@app.get("/student/classes", response_model=List[schemas.Class])
def get_student_classes(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_student_user)):
    return crud.get_student_classes(db, current_user.id)

@app.get("/student/assignments", response_model=List[schemas.Assignment])
def get_assignments_for_student(db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_student_user)):
    return crud.get_assignments_for_student(db, current_user.id)

@app.post("/student/assignments/{assignment_id}/submit", response_model=schemas.AssignmentSubmission)
def submit_assignment(assignment_id: int, submission: schemas.SubmissionCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(dependencies.get_student_user)):
    # 学生提交作业
    return crud.submit_assignment(db, assignment_id, submission, current_user.id)
