from schemas.library import LibraryEntry, LibraryResponse, EntryUpdate
from models.library import Library
from core.database import Session
from sqlalchemy import select, update, delete, func
from core.cache import rconn
from redis.exceptions import ConnectionError

def create_entry(entry: LibraryEntry, current_user_id):
    with Session() as session:
        new_entry = Library(user_id=current_user_id, game_id=entry.game_id, status=entry.status)
        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)
    return LibraryResponse(id=new_entry.id, user_id=new_entry.user_id, game_id=new_entry.game_id, status=new_entry.status)

def read_entry(entry_id: int):
    with Session() as session:
        entry = session.execute(select(Library).where(Library.id == entry_id)).scalar_one_or_none()
        if entry:
            return LibraryResponse(id=entry.id, user_id=entry.user_id, game_id=entry.game_id, status=entry.status)
        raise ValueError

def update_entry(updated_entry: EntryUpdate, user_id: int):
    with Session() as session:
        entry = session.execute(select(Library).where(Library.id == updated_entry.id)).scalar_one_or_none()
        if entry:
            if entry.user_id == user_id:
                session.execute(update(Library).where(Library.id == entry.id).values(
                    status=updated_entry.status
                ))
                session.commit()
                return LibraryResponse(id = entry.id, user_id=entry.user_id, game_id=entry.game_id, status=entry.status)
            raise PermissionError
        raise ValueError
        
def delete_entry(entry_id: int, user_id: int):
    with Session() as session:
        entry = session.execute(select(Library).where(Library.id == entry_id)).scalar_one_or_none()
        if entry:
            if entry.user_id == user_id:
                session.execute(delete(Library).where(Library.id == entry_id))
                session.commit()
                return True
            raise PermissionError
        raise ValueError
    
    
def _fetch_trending():
    with Session() as session:
        subq = select(Library.game_id).order_by(Library.id.desc()).limit(50).subquery()
        return session.execute(select(subq.c.game_id, func.count(subq.c.game_id).label('count'))
            .group_by(subq.c.game_id)
            .order_by(func.count(subq.c.game_id).desc())
            .limit(1)).scalar_one_or_none()

def trending_game():
    try:
        game = rconn.get('trending_game')

        if game:
            #print('Jogo encontrado pelo redis') # DEBUG
            return game
        else:
            game_id = _fetch_trending()
            rconn.set('trending_game', game_id, ex=3600)
            return game_id
    except ConnectionError:
        return _fetch_trending()