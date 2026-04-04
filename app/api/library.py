from fastapi import APIRouter, Depends, Response
from services.library import create_entry, read_entry, update_entry, delete_entry
from schemas.library import LibraryEntry, LibraryResponse, EntryUpdate
from services.user import get_current_user
from sqlalchemy.exc import DataError

libraries = APIRouter()

@libraries.post('/library/create', status_code=201)
async def create(entry: LibraryEntry, response: Response, user = Depends(get_current_user)):
    try:
        new_entry = create_entry(entry, user.id)
    except DataError as e:
        response.status_code = 422
        return 'Invalid TAG or PLATFORM.'
    return new_entry

@libraries.get('/library/{entry_id}')
def read(entry_id: int, response: Response, user = Depends(get_current_user)):
    entry = read_entry(entry_id)
    if entry:
        return entry
    response.status_code = 404
    return 'Entry not found.'

@libraries.put('/library/{entry_id}')
def update(entry: EntryUpdate, response: Response, user = Depends(get_current_user)):
    try:
        updated_entry = update_entry(entry)
        if updated_entry:
            return updated_entry
        
        response.status_code = 404
        return 'Entry not found.'
    except DataError as e:
        response.status_code = 422
        return 'Invalid Status.'
    
@libraries.delete('/library/{entry_id}')
def delete(entry_id: int, user = Depends(get_current_user)):
    deleted_entry = delete_entry(entry_id)
    return deleted_entry