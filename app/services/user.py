from schemas.user import UserCreate, UserResponse, UserLogin, UserStatus
from core.database import Session
from models.user import User
from datetime import datetime, timedelta
from pwdlib import PasswordHash
from sqlalchemy import select, func
from env import SECRET_KEY
import jwt
from fastapi.security import HTTPBearer
from fastapi import Depends
from models.review import Review
from models.library import Library


password_hash = PasswordHash.recommended()
oauth2_scheme = HTTPBearer()

def create_user(user: UserCreate):
    with Session() as session:
        date = datetime.now()
        hashed_password = password_hash.hash(user.password)
        new_user = User(name=user.name, email=user.email, password=hashed_password, created_at=date)
        session.add(new_user)
        session.commit()
        # Recarrega os dados do banco
        session.refresh(new_user)
    return UserResponse(id=new_user.id, name=new_user.name, email=new_user.email, created_at=new_user.created_at)
        
        
def login_user(user: UserLogin):
    with Session() as session:
        result = session.execute(select(User).where(User.email == user.email)).scalar_one_or_none()   
        if result:
            match = password_hash.verify(user.password, result.password)
            if match:
                exp = datetime.utcnow() + timedelta(hours=1)
                return jwt.encode({"exp":exp, "user_id":result.id}, SECRET_KEY, algorithm="HS256")
        raise ValueError

def get_current_user(credentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    with Session() as session:
        current_user = session.execute(select(User).where(User.id == payload["user_id"])).scalar_one_or_none()
        if current_user:
            print(current_user)
            return current_user
        
def user_stats(user_name: str):
    with Session() as session:
        searched_user = session.execute(select(User).where(func.lower(User.name) == user_name)).scalar_one_or_none()
        if searched_user:
            games_reviewed = session.execute(select(func.count(Review.id)).where(Review.user_id == searched_user.id)).scalar()
            games_played = session.execute(select(func.count(Library.id)).where(Library.user_id == searched_user.id,
                Library.status != 'WISHLIST', Library.status != 'PLAYING')).scalar()
            games_wishlisted = session.execute(select(func.count(Library.id)).where(Library.user_id == searched_user.id,
                Library.status == 'WISHLIST')).scalar()
            games_playing = session.execute(select(func.count(Library.id)).where(Library.user_id == searched_user.id,
                Library.status == 'PLAYING')).scalar()
            days_since_creation = (datetime.now() - searched_user.created_at).days
            return UserStatus(name=searched_user.name,
                games_reviewed=games_reviewed, games_played=games_played,
                games_wishlisted=games_wishlisted, games_playing=games_playing, 
                days_since_creation=days_since_creation)
        raise ValueError