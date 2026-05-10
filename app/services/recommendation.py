from schemas.game import GameResponse
from models.review import Review
from models.library import Library
from models.game import Game
from core.database import Session
from sqlalchemy import select

def _search_user_highest_rated_games(user_id: int):
    with Session() as session:
        games = session.execute(select(Review.game_id).where(Review.user_id == user_id)
            .order_by(Review.stars.desc()).limit(3)).scalars().all()
    return games
        
def _search_game_tags(games: list):
    with Session() as session:
        game_tags = session.execute(select(Game.tag)
            .where(Game.id.in_(games))).scalars().all()
    return game_tags

def _search_all_user_games(user_id: int):
    with Session() as session:
        games = session.execute(select(Library.game_id).where(Library.user_id == user_id)
            ).scalars().all()
    return games

def recommend_games(user_id: int):
    games = _search_user_highest_rated_games(user_id)
    
    if not games:
        raise ValueError
    
    all_user_games = _search_all_user_games(user_id)

    if not all_user_games:
        raise ValueError
    
    tags = _search_game_tags(games)
    
    with Session() as session:
        recommendations = session.execute(select(Game).where(Game.id.not_in(all_user_games), 
            Game.tag.in_(tags)).limit(5)).scalars().all()
    
    rec_list = []

    for recommendation in recommendations:
        rec_list.append(GameResponse(id=recommendation.id, name=recommendation.name,
            description=recommendation.description, tag=recommendation.tag,
            platform=recommendation.platform))
    return rec_list

