from datetime import datetime
import email
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: str
    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserFetchByIdResponse(UserCreateResponse):
    pass

class UserLogin(UserCreate):
    pass