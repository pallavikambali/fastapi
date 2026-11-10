
from pydantic import BaseModel,EmailStr,ConfigDict,Field
from datetime import datetime
from typing import Optional, List,Annotated
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  


class Post(PostBase):
    id: int
    title: str
    content: str
    created_at:datetime
    owner_id: int
    owner: UserOut  # Reference to the User model

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    password: str
    model_config = ConfigDict(from_attributes=True)



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]  # dir can only be 0 or 1, where 1 means upvote and 0 means remove vote


class PostOut(BaseModel):
    Post: Post
    vote_count: int

    model_config = ConfigDict(from_attributes=True)