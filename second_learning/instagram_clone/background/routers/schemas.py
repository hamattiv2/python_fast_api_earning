from datetime import datetime
from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    
class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    
    class Config():
        orm_mode = True

class Comment(BaseModel):
    username: str
    text: str
    timestamp: datetime
    
    class Config():
        orm_mode = True

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creater_id: int


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserDisplay
    comments: List[Comment]
    
    class Config():
        orm_mode = True

        
