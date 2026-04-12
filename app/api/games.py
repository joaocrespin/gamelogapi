from fastapi import APIRouter, Depends, status, Response, HTTPException
from services.game import create_game, read_game, update_game, delete_game
from schemas.game import GameCreate, GameResponse
from models.game import Game
from sqlalchemy.exc import DataError
from services.user import get_current_user

games = APIRouter()

# Depends para proteção das rotas (exige token)
@games.post('/games/create', status_code=201)
async def create(game: GameCreate, response: Response, user = Depends(get_current_user)):
    try:
        new_game = create_game(game)
    except DataError as e:
        response.status_code = 422
        return 'Invalid TAG or PLATFORM.', e
    return new_game

@games.get('/games/{game_id}')
def read(game_id: int, response: Response, user = Depends(get_current_user)):
    try: 
        game = read_game(game_id)
        return game
    except ValueError:
        raise HTTPException(status_code=404, detail='Game not found')

@games.put('/games/{game_id}')
def update(game: GameResponse, response: Response, user = Depends(get_current_user)):
    try:
        updated_game = update_game(game)
        return updated_game
    except DataError as e:
        response.status_code = 422
        return 'Invalid TAG or PLATFORM.'
    except ValueError:
        raise HTTPException(status_code=404, detail='Game not found')
    
@games.delete('/game/{game_id}')
def delete(game_id: int, response: Response, user = Depends(get_current_user)):
    try:
        delete_game(game_id)
        response.status_code = 204
        return 'Deleted successfully'
    except ValueError:
        raise HTTPException(status_code=404, detail='Game not found')