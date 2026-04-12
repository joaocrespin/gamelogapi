from pydantic import BaseModel
from models.library import Status

class LibraryEntry(BaseModel):
    #user_id: int
    game_id: int
    status: Status

class LibraryResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    status: Status

class EntryUpdate(BaseModel):
    id:int
    status: Status