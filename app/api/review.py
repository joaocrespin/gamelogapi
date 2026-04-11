from fastapi import APIRouter, Depends, Response
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
    review = read_review(review_id)
    if review:
        return review
    
    response.status_code = 404
    return 'Review not found.'

@reviews.put('/review/{review_id}')
def update(review: ReviewUpdate,  response: Response, user = Depends(get_current_user)):
    review = update_review(review)
    if review:
        return review
    
    response.status_code = 404
    return 'Review not found.'

@reviews.delete('/review/{review_id}')
def delete(review_id: int,  response: Response, user = Depends(get_current_user)):
    deleted_review = delete_review(review_id)
    return deleted_review