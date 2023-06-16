from sqlalchemy.orm import Session
from flask import request
from app.dao import Todo
from app.dao import User
from app.base.main import get_engine
from app.dto.todo import TodoInfo
engine = get_engine()


class TodoModel:

    def __fetch_todo(self, **kwargs):
        with Session(engine) as session:
            user = session.query(User).filter(User.username == kwargs.get("username")).first()
            all_todo = (session.query(Todo).filter(
                Todo.user == user,
                Todo.is_completed == kwargs.get("completed")
            ).order_by(Todo.created_at.desc())
                        )
        return all_todo

    def fetch_completed_todo(self, username: str):
        return self.__fetch_todo(username = username, completed=False)

    def fetch_incomplete_todo(self, username: str):
        return self.__fetch_todo(username = username, completed=True)

    def update_completed(self, update_status: bool, todo_id: int) -> bool:
        is_updated = False
        with Session(engine) as session:
            todo = session.query(Todo).where(Todo.id == todo_id).first()
            if todo is not None:
                todo.is_completed = update_status
                is_updated = True
                session.commit()

        return is_updated

    def create_todo(self, todo_info: TodoInfo) -> bool:
        is_created = False
        with Session(engine) as session:
            user_name = request.cookies.get("username")

            user = session.query(User).filter(User.username == user_name ).first()
            todo = Todo(
                title=todo_info.title,
                desc=todo_info.description,
                user = user
            )

            session.add(todo)

            session.commit()
            is_created = True

        return is_created

    def delete_todo(self, todo_id: int ) -> bool:
        delete_status = False
        with Session(engine) as session:
            session.query(Todo).where(Todo.id == todo_id).delete()
            session.commit()
            delete_status = True

        return delete_status
