from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from passlib.context import CryptContext

from app.db.dep import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserOut

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_id=str(uuid4())
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
