from fastapi import APIRouter, HTTPException, Depends
from services.library import trending_game
from services.game import read_game
from redis.exceptions import DataError
from services.recommendation import recommend_games
from services.user import get_current_user

insights = APIRouter()

@insights.get('/trending/game')
def trending():
    try:
        tg = trending_game()
        game = read_game(tg)
        return game
    except DataError:
        raise HTTPException(status_code=404, detail='No trending game at the moment.')
    
@insights.get('/recommendations')
def recommendations(user = Depends(get_current_user)):
    try:
        recommended = recommend_games(user.id)
        return recommended
    except ValueError:
        raise HTTPException(status_code=404, detail='You need to add a game to library '
        'or review a geme before getting recommendations.')