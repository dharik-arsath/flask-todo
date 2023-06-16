from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.base.main import get_engine
from app.dao import User

engine = get_engine()
from app.user.password_manager.main import PasswordGenerator

pass_gen = PasswordGenerator()
@dataclass
class UserInfo:
    username : str = ""
    password : str = ""


class UserModel:
    def create_new_user(self, user_info: UserInfo) -> None:
        hashed_password: str = pass_gen.hash_password(user_info.password.encode("utf-8"))
        with Session(engine) as session:
            new_user = User(
                username = user_info.username,
                password = hashed_password
            )

            session.add(new_user)
            session.commit()

    def validate_user(self, user_info : UserInfo) -> bool:
        with Session(engine) as session:
            user = session.query(User).filter(User.username == user_info.username).first()
            is_valid_credential = False
            if user is not None:
                is_valid_credential = user.validate_password(user_info.password)

        return is_valid_credential
