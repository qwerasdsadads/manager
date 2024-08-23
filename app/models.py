from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


# 用户模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, force_index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)
    password = Column(String)

    # Relationships
    teachers = relationship("Teacher", back_populates="user")
    students = relationship("Student", back_populates="user")


# 用户基础信息模型
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

# 教师模型
class TeacherBase(BaseModel):
    name: str
    email: str

class TeacherCreate(TeacherBase):
    password: str

class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True

# 学生模型
class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

# 班级模型
class ClassBase(BaseModel):
    name: str
    teacher_id: int

class ClassCreate(ClassBase):
    pass
class Class(ClassBase):
    id: int
    students: List[Student] = []

    class Config: 
        from_attributes = True

# 作业模型
class AssignmentBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    class_id: int

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    submissions: List['AssignmentSubmission'] = []

    class Config:
        from_attributes = True

# 作业提交模型
class AssignmentSubmissionBase(BaseModel):
    file: str
    remarks: Optional[str] = None

class AssignmentSubmissionCreate(AssignmentSubmissionBase):
    pass

class AssignmentSubmission(AssignmentSubmissionBase):
    id: int
    student_id: int
    assignment_id: int

    class Config:
        from_attributes = True

# Token 数据模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str
