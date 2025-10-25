# app/services/user_services.py

from sqlalchemy.orm import Session
from app.models import users as user_model
from app.schemas.users import UserUpdate

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        return None

    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = user_update.password  # تأكد من التشفير لو تستعمله
    db.commit()
    db.refresh(user)
    return user
