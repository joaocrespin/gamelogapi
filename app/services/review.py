from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from models.review import Review
from core.database import Session
from sqlalchemy import select, update, delete

def create_review(review: ReviewCreate, user_id: int):
    with Session() as session:
        new_review = Review(user_id=user_id, game_id=review.game_id,
            stars=review.stars, review=review.review)
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
    return ReviewResponse(id=new_review.id, user_id=new_review.user_id, 
        game_id=new_review.game_id, stars=new_review.stars, review=new_review.review)

def read_review(review_id: int):
    with Session() as session:
        review = session.execute(select(Review).where(Review.id == review_id)).scalar_one_or_none()
        if review:
            return ReviewResponse(id=review.id, user_id=review.user_id, 
        game_id=review.game_id, stars=review.stars, review=review.review)

def update_review(updated_review: ReviewUpdate):
    with Session() as session:
        review = session.execute(select(Review).where(Review.id == updated_review.id)).scalar_one_or_none()
        if review:
            session.execute(update(Review).where(Review.id == review.id).values(
                stars=updated_review.stars, review=updated_review.review
            ))
            session.commit()
            return ReviewResponse(id=review.id, user_id=review.user_id, game_id=review.game_id,
                                  stars=review.stars, review=review.review)

def delete_review(review_id: int):
    with Session() as session:
        session.execute(delete(Review).where(Review.id == review_id))
        session.commit()
        return 'Deleted sucessfully.'