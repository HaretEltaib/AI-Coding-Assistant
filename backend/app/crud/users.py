from sqlalchemy.orm import Session 
from fastapi import HTTPException
from app.models.users import User as UserModel
from app.schemas.users import UserCreate, UserUpdate
from uuid import UUID
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user_create: UserCreate):
    existing_user = db.query(UserModel).filter(UserModel.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_create.password)

    db_user = UserModel(
        name=user_create.name,
        email=user_create.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_uuid: UUID):
    user = db.query(UserModel).filter(UserModel.uuid == str(user_uuid)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserModel).offset(skip).limit(limit).all()

def update_user(db: Session, user_uuid: UUID, user_update: UserUpdate):
    user = get_user(db, user_uuid)
    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        user.email = user_update.email
    db.commit()
    db.refresh(user)
    return user

def user_delete(db: Session, user_uuid: UUID):
    user = get_user(db, user_uuid)
    user_name = user.name
    db.delete(user)
    db.commit()
    return {"ok": True, "message": f"User '{user_name}' deleted"}
