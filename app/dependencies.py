from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import crud, schemas
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.models import User
# 配置
SECRET_KEY = "your-secret-key"  # 请替换为实际的密钥
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 密码加密和验证上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token 数据模型
class TokenData(BaseModel):
    username: str
    role: str

# 从 Token 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "unknown")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 获取管理员用户
def get_admin_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user

# 获取教师用户
def get_teacher_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user

# 获取学生用户
def get_student_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if current_user.role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user

# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 哈希密码
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def delete_user(db: Session, user_id: int) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise ValueError("User not found")