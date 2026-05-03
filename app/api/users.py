from fastapi import APIRouter, Depends, HTTPException
from services.user import create_user, login_user, get_current_user, user_stats
from schemas.user import UserCreate, UserLogin, Token
from models.user import User
from sqlalchemy.exc import IntegrityError

users = APIRouter()

@users.post('/user/register')
async def register(user: UserCreate):
   try:
      new_user = create_user(user)
      return new_user
   except IntegrityError:
         raise HTTPException(status_code=409, detail='Username already in use.')

@users.post('/user/login')
async def login(user: UserLogin):
   try:
      result = login_user(user)
      if result:
         return Token(access_token=result, token_type="Bearer")
   except ValueError:
      raise HTTPException(status_code=401, detail='Incorrect username or password.')
   
   
@users.get('/user/me')
async def profile(user: User = Depends(get_current_user)):
    return {
       "name": user.name,
       "email": user.email,
       "created_at": user.created_at
    }

@users.get('/status/')
def stats(user_name: str):
    try:
        user_statistics = user_stats(user_name)
        return user_statistics
    except ValueError:
        raise HTTPException(status_code=404, detail='User not found.')