from pydantic import BaseModel
from models.library import Library

class LibraryEntry(BaseModel):
    #user_id: int
    game_id: int
    status: str

class LibraryResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    status: str

class EntryUpdate(BaseModel):
    id:int
    status: str