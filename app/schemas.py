from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 登录相关模式
class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

# 用户相关模式
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# 教师相关模式
class TeacherBase(BaseModel):
    name: str
    email: str

class TeacherCreate(TeacherBase):
    password: str

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True

# 学生相关模式
class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

# 班级相关模式
class ClassBase(BaseModel):
    name: str

class ClassCreate(ClassBase):
    teacher_id: int

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None

class Class(ClassBase):
    id: int

    class Config:
        from_attributes = True

# 作业相关模式
class AssignmentBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime

class AssignmentCreate(AssignmentBase):
    class_id: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    class_id: Optional[int] = None

class Assignment(AssignmentBase):
    id: int

    class Config:
        from_attributes = True

# 作业提交相关模式
class SubmissionBase(BaseModel):
    file: str
    remarks: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    student_id: int
    assignment_id: int

class Submission(SubmissionBase):
    id: int

    class Config:
        from_attributes = True

# 登录时的 token 数据模式
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

class AssignmentSubmissionBase(BaseModel):
    file: str
    remarks: Optional[str] = None

class AssignmentSubmissionCreate(AssignmentSubmissionBase):
    student_id: int
    assignment_id: int

class AssignmentSubmission(AssignmentSubmissionBase):
    id: int

    class Config:
        from_attributes = True
