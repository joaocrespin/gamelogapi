from pydantic import BaseModel
from models.game import Tags, Platforms

class GameCreate(BaseModel):
    name: str
    description: str
    tag: Tags
    platform: Platforms

class GameResponse(BaseModel):
    id: int
    name: str
    description: str
    tag: Tags
    platform: Platforms