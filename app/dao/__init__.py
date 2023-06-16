from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.base import get_engine
from app.user.password_manager.main import PasswordGenerator
from app.dao.todo import dao
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import DateTime, Boolean
from sqlalchemy import ForeignKey
from typing import Optional
import datetime

engine      = get_engine()
pass_gen    = PasswordGenerator()


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
    # created_at      : Mapped[datetime]          = Column(DateTime, default=datetime.datetime.utcnow)
    created_at      : Mapped[datetime]          = mapped_column(DateTime, default=datetime.datetime.now)
    is_completed    : Mapped[bool]              = mapped_column(Boolean, default=False)

    user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))
    user            : Mapped["User"]            = relationship(back_populates="todo")



Base.metadata.create_all(engine)

