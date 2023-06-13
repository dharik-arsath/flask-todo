import datetime
from typing import Optional

from sqlalchemy import String, Column, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.base.main import get_engine

engine = get_engine()


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__      = "Todo"

    id              : Mapped[int]               = mapped_column(primary_key = True)
    title           : Mapped[str]               = mapped_column(String(60))
    desc            : Mapped[Optional[str] ]
    created_at      : Mapped[datetime]          = Column(DateTime, default=datetime.datetime.utcnow)
    is_completed    : Mapped[bool]              = Column(Boolean, default=False)


Base.metadata.create_all(engine)

