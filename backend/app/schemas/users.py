from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str 

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserOut(UserBase):
    uuid: UUID

    model_config = {
        "from_attributes": True
    }
