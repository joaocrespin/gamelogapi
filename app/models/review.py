from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

class Review(Base):
    __tablename__='reviews'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'))
    stars: Mapped[int] = mapped_column()
    review: Mapped[str] = mapped_column(String)