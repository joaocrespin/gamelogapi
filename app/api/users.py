from fastapi import APIRouter, Depends
from services.user import create_user, login_user, get_current_user
from schemas.user import UserCreate, userLogin, Token
from models.user import User

users = APIRouter()

@users.post('/user/register')
async def register(user: UserCreate):
   new_user = create_user(user)
   return new_user

@users.post('/user/login')
async def login(user: userLogin):
   result = login_user(user)
   if result:
      return Token(access_token=result, token_type="Bearer")
   
@users.get('/user/me')
async def profile(user: User = Depends(get_current_user)):
    return {
       "name": user.name,
       "email": user.email,
       "created_at": user.created_at
    }