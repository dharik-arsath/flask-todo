import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String, INT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Boolean
from app.base.main import Base, DEFAULT_DATETIME

from app.utils.main import slugify as utils_slug

class Todo(Base):
    __tablename__      = "Todo"

    id              : Mapped[int]               = mapped_column(primary_key = True)
    title           : Mapped[str]               = mapped_column(String(60))
    desc            : Mapped[Optional[str] ]
    priority        : Mapped[int]               = mapped_column(INT, default=0)

    created_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    is_completed    : Mapped[bool]              = mapped_column(Boolean, default=False)

    workspace       : Mapped[int]               = mapped_column(ForeignKey("Workspace.id"))
    user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))
    user            : Mapped["User"]            = relationship(back_populates="todo")



class Workspace(Base):
    __tablename__ = "Workspace"

    id              : Mapped[int]               = mapped_column(primary_key=True)
    title           : Mapped[int]               = mapped_column(String(60), unique=False)
    desc            : Mapped[Optional[str]]
    url             : Mapped[str]               = mapped_column(String(200), unique=False)
    slug            : Mapped[str]               = mapped_column(String(150), unique=False)
    created_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    updated_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))

    @property
    def title_slug(self):
        return utils_slug(self.title)

