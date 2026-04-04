from schemas.library import LibraryEntry, LibraryResponse, EntryUpdate
from models.library import Library
from core.database import Session
from sqlalchemy import select, update, delete

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
    return LibraryResponse(id=entry.id, user_id=entry.user_id, game_id=entry.game_id, status=entry.status)

def update_entry(updated_entry: EntryUpdate):
    with Session() as session:
        entry = session.execute(select(Library).where(Library.id == updated_entry.id)).scalar_one_or_none()
        if entry:
            session.execute(update(Library).where(Library.id == entry.id).values(
                status=updated_entry.status
            ))
            session.commit()
            return LibraryResponse(id = entry.id, user_id=entry.user_id, game_id=entry.game_id, status=entry.status)
        
def delete_entry(entry_id: int):
    with Session() as session:
        session.execute(delete(Library).where(Library.id == entry_id))
        session.commit()
        return 'Deleted sucessfully.'