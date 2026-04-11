from models import game, library, review, user
from core.database import Base, engine
from fastapi import FastAPI
from api.users import users
from api.games import games
from api.library import libraries
from api.review import reviews

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users)
app.include_router(games)
app.include_router(libraries)
app.include_router(reviews)