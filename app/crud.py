# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, role=user.role, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 获取所有用户
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# 根据ID获取用户
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 创建教师
def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(name=teacher.name, email=teacher.email, password=teacher.password)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# 获取所有教师
def get_teachers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

# 根据ID获取教师
def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

# 创建学生
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, email=student.email, password=student.password)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# 获取所有学生
def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student).offset(skip).limit(limit).all()

# 根据ID获取学生
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# 创建班级
def create_class(db: Session, class_: schemas.ClassCreate):
    db_class = models.Class(name=class_.name)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

# 获取所有班级
def get_classes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Class).offset(skip).limit(limit).all()

# 根据ID获取班级
def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()

# 创建作业
def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(
        title=assignment.title,
        description=assignment.description,
        start_date=assignment.start_date,
        end_date=assignment.end_date,
        class_id=assignment.class_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# 获取所有作业
def get_assignments(db: Session, class_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Assignment).filter(models.Assignment.class_id == class_id).offset(skip).limit(limit).all()

# 创建作业提交
def submit_assignment(db: Session, assignment_id: int, student_id: int, submission: schemas.AssignmentSubmissionCreate):
    db_submission = models.AssignmentSubmission(
        file=submission.file,
        remarks=submission.remarks,
        student_id=student_id,
        assignment_id=assignment_id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission
