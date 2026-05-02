from schemas.game import GameCreate, GameResponse
from models.game import Game, Tags, Platforms
from core.database import Session
from sqlalchemy import select, update, delete, func

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
        raise ValueError
        
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
        raise ValueError
        
def delete_game(game_id: int):
    with Session() as session:
        if session.execute(select(Game.id).where(Game.id == game_id)).scalar_one_or_none():
            session.execute(delete(Game).where(Game.id == game_id))
            session.commit()
            return True
        raise ValueError
    
def search_game(name: str = None, platform: Platforms = None, tag: Tags = None):
    with Session() as session:
        if platform is None and tag is None:
            game = session.execute(select(Game).where(func.lower(Game.name).like(f'{name}%'))).scalars().all()
        elif name is None and tag is None:
            game = session.execute(select(Game).where(Game.platform == platform)).scalars().all()
        elif name is None and platform is None:
            game = session.execute(select(Game).where(Game.tag == tag)).scalars().all()
        elif tag is None:
            game = session.execute(select(Game).where(func.lower(Game.name).like(f'{name}%')
                , Game.platform == platform)).scalars().all()
        elif platform is None:
            game = session.execute(select(Game).where(func.lower(Game.name).like(f'{name}%')
                , Game.tag == tag)).scalars().all()
        elif name is None:
            game = session.execute(select(Game).where(Game.platform == platform
                , Game.tag == tag)).scalars().all()
        else: 
            game = session.execute(select(Game).where(func.lower(Game.name).like(f'{name}%')
                    , Game.platform == platform, Game.tag == tag)).scalars().all()
        if game:
            return game
        raise ValueError