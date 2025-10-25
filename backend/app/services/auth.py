from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import User
from app.db.dep import get_db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas.token import TokenData

# إعدادات التشفير
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# إعدادات التوكن
SECRET_KEY = "your_secret_key_here"  # غيّرها لقيمة قوية فعلية
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str, by_name: bool = False):
    # تم تعديل هذا الجزء ليعتمد على البريد الإلكتروني بشكل افتراضي
    if by_name:
        user = db.query(User).filter(User.name == username).first()
    else:
        user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token: no subject")
        return TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
