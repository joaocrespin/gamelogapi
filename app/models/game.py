from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as dbEnum
from enum import Enum

class Tags(Enum):
    RPG = 'RPG'
    ACTION = 'ACTION'
    ADVENTURE = 'ADVENTURE'
    SIMULATION ='SIMULATION'
    CASUAL='CASUAL'
    ROMANCE='ROMANCE'

class Platforms(Enum):
    XBOX = 'xbox'
    PC='pc'
    PLAYSTATION='playstation'
    SEGA='saturn'

class Game(Base):
    __tablename__='games'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    tag: Mapped[Tags] = mapped_column(dbEnum(Tags))
    platform: Mapped[Platforms] = mapped_column(dbEnum(Platforms))