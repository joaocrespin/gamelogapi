from fastapi import APIRouter, HTTPException
from services.library import trending_game
from services.game import read_game
from redis.exceptions import DataError

trends = APIRouter()

@trends.get('/trending/game')
def trending():
    try:
        tg = trending_game()
        game = read_game(tg)
        return game
    except DataError:
        raise HTTPException(status_code=404, detail='No trending game at the moment.')
    