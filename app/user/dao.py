from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.base import get_engine
from app.base import Base
from app.user.password_manager.main import PasswordGenerator

engine      = get_engine()
pass_gen    = PasswordGenerator()


class User(Base):

    __tablename__   = "User"

    id              : Mapped[int]               = mapped_column(primary_key = True)
    username        : Mapped[str]               = mapped_column(String(100))
    password        : Mapped[str]               = mapped_column(String(100))

    def validate_password(self, password: str) -> bool:
        print("checking passowr.d..")
        print(self.password, password)
        print(self.username)
        pass_hash = pass_gen.hash_password(password.encode('utf-8'))
        return self.password == pass_hash


Base.metadata.create_all(engine)

