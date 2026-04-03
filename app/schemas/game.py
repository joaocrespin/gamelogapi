from pydantic import BaseModel

class GameCreate(BaseModel):
    name: str
    description: str
    tag: str
    platform: str

class GameResponse(BaseModel):
    id: int
    name: str
    description: str
    tag: str
    platform: str