from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime
#from app.models.answers import Answer

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    answers: Mapped[list['Answer']] = relationship('Answer', back_populates='question', cascade='all, delete-orphan')