from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email: str
    password: str


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