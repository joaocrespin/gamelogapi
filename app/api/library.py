from fastapi import APIRouter, Depends, Response, HTTPException
from services.library import create_entry, read_entry, update_entry, delete_entry
from schemas.library import LibraryEntry, LibraryResponse, EntryUpdate
from services.user import get_current_user
from sqlalchemy.exc import DataError, IntegrityError

libraries = APIRouter()

@libraries.post('/library/create', status_code=201)
async def create(entry: LibraryEntry, response: Response, user = Depends(get_current_user)):
    try:
        new_entry = create_entry(entry, user.id)
    except DataError as e:
        raise HTTPException(status_code=422, detail='Invalid TAG or PLATFORM.')
    except IntegrityError:
        raise HTTPException(status_code=422, detail='Game not found.')
    return new_entry

@libraries.get('/library/{entry_id}')
def read(entry_id: int, response: Response, user = Depends(get_current_user)):
    try:
        entry = read_entry(entry_id)
        return entry
    except ValueError:
        raise HTTPException(status_code=404, detail='Entry not found')
   

@libraries.put('/library/{entry_id}')
def update(entry: EntryUpdate, response: Response, user = Depends(get_current_user)):
    try:
        updated_entry = update_entry(entry, user.id)
        if updated_entry:
            return updated_entry
    except DataError as e:
        response.status_code = 422
        return 'Invalid Status.'
    except ValueError:
        raise HTTPException(status_code=404, detail='Entry not found')
    except PermissionError:
        raise HTTPException(status_code=403, detail=
            'You do not have permission to perform this action.')
    
    
@libraries.delete('/library/{entry_id}')
def delete(entry_id: int, response: Response, user = Depends(get_current_user)):
    try:
        delete_entry(entry_id, user.id)
        response.status_code = 204
        return 'Deleted successfully'
    except ValueError:
        raise HTTPException(status_code=404, detail='Entry not found') 
    except PermissionError:
        raise HTTPException(status_code=403, detail=
            'You do not have permission to perform this action.')