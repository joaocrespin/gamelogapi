from fastapi import APIRouter, Depends, Response, HTTPException
from services.review import create_review, read_review, update_review, delete_review
from schemas.review import ReviewCreate, ReviewUpdate
from services.user import get_current_user
from sqlalchemy.exc import IntegrityError

reviews = APIRouter()

@reviews.post('/review/create', status_code=201)
async def create(review: ReviewCreate, response: Response, user = Depends(get_current_user)):
    try:
        new_review = create_review(review, user.id)
        return new_review
    except IntegrityError:
        response.status_code = 404
        return 'Game not found!'

@reviews.get('/review/{review_id}')
def read(review_id: int,  response: Response, user = Depends(get_current_user)):
    try:
        review = read_review(review_id)
        return review
    except ValueError:
        raise HTTPException(status_code=404, detail='Review not found')

@reviews.put('/review/{review_id}')
def update(review: ReviewUpdate,  response: Response, user = Depends(get_current_user)):
    try:
        review = update_review(review, user.id)
        return review
    except ValueError:
        raise HTTPException(status_code=404, detail='Review not found')
    except PermissionError:
        raise HTTPException(status_code=403, detail=
            'You do not have permission to perform this action.')
    
    
@reviews.delete('/review/{review_id}')
def delete(review_id: int,  response: Response, user = Depends(get_current_user)):
    try:
        delete_review(review_id, user.id)
        response.status_code = 204
        return 'Deleted successfully'
    except ValueError:
        raise HTTPException(status_code=404, detail='Review not found')
    except PermissionError:
        raise HTTPException(status_code=403, detail=
            'You do not have permission to perform this action.')
    