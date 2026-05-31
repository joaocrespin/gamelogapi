from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    name:str
    email: str
    created_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserStatus(BaseModel):
    name: str
    games_reviewed: int
    games_played: int
    games_wishlisted: int
    games_playing: int
    days_since_creation: int