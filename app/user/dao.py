from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.base.main import Base, DEFAULT_DATETIME
from app.user.password_manager.main import PasswordGenerator
from app.todo.dao import Todo

pass_gen = PasswordGenerator()

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