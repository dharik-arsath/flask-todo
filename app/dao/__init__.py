from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.base import get_engine
from app.user.password_manager.main import PasswordGenerator
from app.dao.todo import dao
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import DateTime, Boolean
from sqlalchemy import ForeignKey, func
from app.utils.main import slugify as utils_slug
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import deferred

from typing import Optional
import datetime

engine      = get_engine()
pass_gen    = PasswordGenerator()


DEFAULT_DATETIME = datetime.datetime.now

class Base(DeclarativeBase):
    pass



class User(Base):

    __tablename__   = "User"

    id              : Mapped[int]               = mapped_column(primary_key = True)
    username        : Mapped[str]               = mapped_column(String(100))
    password        : Mapped[str]               = mapped_column(String(100))
    todo            : Mapped[List["Todo"]]      = relationship(back_populates="user")

    def validate_password(self, password: str) -> bool:
        print("checking passowr.d..")
        pass_hash = pass_gen.hash_password(password.encode('utf-8'))
        print(self.password, pass_hash)
        return self.password == pass_hash


class Todo(Base):
    __tablename__      = "Todo"

    id              : Mapped[int]               = mapped_column(primary_key = True)
    title           : Mapped[str]               = mapped_column(String(60))
    desc            : Mapped[Optional[str] ]
    created_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    is_completed    : Mapped[bool]              = mapped_column(Boolean, default=False)

    workspace       : Mapped[int]               = mapped_column(ForeignKey("Workspace.id"))
    user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))
    user            : Mapped["User"]            = relationship(back_populates="todo")



class Workspace(Base):
    __tablename__ = "Workspace"

    id              : Mapped[int]               = mapped_column(primary_key=True)
    title           : Mapped[int]               = mapped_column(String(60), unique=True)
    desc            : Mapped[Optional[str]]
    url             : Mapped[str]               = mapped_column(String(200), unique=True)
    slug            : Mapped[str]               = mapped_column(String(150), unique=True)
    created_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    updated_at      : Mapped[datetime]          = mapped_column(DateTime, default=DEFAULT_DATETIME)
    user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))

    @property
    def title_slug(self):
        return utils_slug(self.title)

Base.metadata.create_all(engine)

