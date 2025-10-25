from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserCreate, UserUpdate, UserOut
from app.schemas.token import Token
from app.db.dep import get_db
from app.crud.users import create_user, get_user, get_users, update_user, user_delete
from app.services.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserOut)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user_create=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # تم التعديل هنا لاستخدام البريد الإلكتروني بدلاً من الاسم
    user = authenticate_user(db, username=form_data.username, password=form_data.password, by_name=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},  # استخدم البريد الإلكتروني داخل الـ Token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/get/{user_uuid}", response_model=UserOut)
def user_get(user_uuid: UUID, db: Session = Depends(get_db)):
    return get_user(user_uuid=user_uuid, db=db)

@router.get("/getAll", response_model=list[UserOut])
def users_get_all(db: Session = Depends(get_db)):
    return get_users(db=db)

@router.patch("/update/{user_uuid}", response_model=UserOut)
def user_update(user_uuid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db=db, user_uuid=user_uuid, user_update=user_update)

@router.delete("/delete/{user_uuid}")
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)):
    return user_delete(user_uuid=user_uuid, db=db)
