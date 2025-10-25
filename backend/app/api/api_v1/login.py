from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.dep import get_db
from app.models.users import User
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

router = APIRouter()

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid login credentials")
    token = create_access_token({"sub": user.email})
    return {
        "status": 200,
        "access_token": token,
        "token_type": "bearer"
    }
