from schemas.game import GameCreate, GameResponse
from models.game import Game
from core.database import Session
from sqlalchemy.exc import DataError
from sqlalchemy import select, update, delete

def create_game(game: GameCreate):
    with Session() as session:
        new_game = Game(name=game.name, description=game.description, tag=game.tag, platform=game.platform)
        session.add(new_game)
        session.commit()
        session.refresh(new_game)
    return GameResponse(id=new_game.id, name=game.name, description=game.description, tag=game.tag, platform=game.platform)

def read_game(game_id: int):
    with Session() as session:
        game = session.execute(select(Game).where(Game.id == game_id)).scalar_one_or_none()
        if game:
            return GameResponse(id=game.id, name=game.name, description=game.description, 
                                tag=game.tag, platform=game.platform)
        
def update_game(game: GameResponse):
    with Session() as session:
        if session.execute(select(Game.id).where(Game.id == game.id)).scalar_one_or_none():
            session.execute(update(Game).where(Game.id == game.id).values(
                name=game.name, description=game.description, tag=game.tag,
                platform=game.platform
            ))
            session.commit()
            return GameResponse(id=game.id, name=game.name, 
                description=game.description, tag=game.tag, platform=game.platform)
        
def delete_game(game_id: int):
    with Session() as session:
        session.execute(delete(Game).where(Game.id == game_id))
        session.commit()
        return 'Deleted sucessfully.'