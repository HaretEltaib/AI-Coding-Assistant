from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dep import get_db
from app.models.users import User
from app.crud.users import update_user, delete_user as user_delete
from app.schemas.users import UserUpdate

router = APIRouter()

@router.patch("/update/{user_id}")
def user_update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db=db, user_id=user_id, user_update=user_update)

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_delete(user_id=user_id, db=db)

@router.get("/get_by_uid/{user_id}")
def get_user_by_user_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
