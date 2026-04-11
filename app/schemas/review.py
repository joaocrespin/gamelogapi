from pydantic import BaseModel

class ReviewCreate(BaseModel):
    game_id: int
    stars: int
    review: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    stars: int
    review: str

class ReviewUpdate(BaseModel):
    id: int
    stars:int
    review: str