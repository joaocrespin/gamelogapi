from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum as dbEnum
from enum import Enum

class Status(Enum):
    PLAYING = 'playing'
    COMPLETED = 'completed'
    DROPPED = 'dropped'
    WISHLIST = 'wishlist'

class Library(Base):
    __tablename__='game_library'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'))
    status: Mapped[Status] = mapped_column(dbEnum(Status))