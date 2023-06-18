import datetime

from flask import request
from sqlalchemy.orm import Session

from app.base.main import get_engine
from .dao import Todo, Workspace
from .dto import TodoInfo, WorkspaceInfo
from app.user import dao

engine = get_engine()

class TodoModel:
    def __fetch_todo(self, **kwargs):
        print(f"----------------------------------------------------------------------------------------------------got {kwargs}")
        with Session(engine) as session:
            user        = session.query(dao.User).filter(dao.User.username == kwargs.get("username")).first()
            workspace   = session.query(Workspace).filter(Workspace.slug == kwargs.get("workspace")).first()

            all_todo = (session.query(Todo).filter(
                Todo.user == user,
                Todo.is_completed == kwargs.get("completed"),
                Todo.workspace == workspace.id
            ).order_by(Todo.created_at.desc())
                        )
        return all_todo

    def fetch_completed_todo(self, username: str, workspace: str):
        return self.__fetch_todo(username = username, workspace=workspace, completed=True)

    def fetch_incomplete_todo(self, username: str, workspace: str):
        return self.__fetch_todo(username = username, workspace = workspace, completed=False)

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

            user        = session.query(dao.User).filter(dao.User.username == user_name ).first()
            workspace   = session.query(Workspace).filter(Workspace.slug == todo_info.workspace).first()

            workspace.updated_at = datetime.datetime.now()
            todo = Todo(
                title=todo_info.title,
                desc=todo_info.description,
                user = user,
                workspace = workspace.id
            )

            session.add(todo)

            session.commit()
            is_created = True

        return is_created


    def update_todo(self, todo_info: TodoInfo) -> bool:
        is_edited = False
        print("----------------------------------update -todo -----------------------------")
        with Session(engine) as session:
            workspace   = session.query(Workspace).filter(Workspace.slug == todo_info.workspace).first()

            todo = session.query(Todo).where(Todo.id == todo_info.id).first()
            if todo is not None:
                print
                todo.title = todo_info.title
                todo.desc  = todo_info.description
                workspace.updated_at = datetime.datetime.now()
                session.commit()
                is_edited = True

        return is_edited

    def delete_todo(self, todo_id: int, workspace_name: str ) -> bool:
        delete_status = False
        with Session(engine) as session:
            session.query(Todo).where(Todo.id == todo_id).delete()
            session.commit()
            delete_status = True

        return delete_status


class WorkspaceModel:
    def add_workspace(self, workspace_info: WorkspaceInfo):
        insert_status = False
        with Session(engine) as session:
            user = session.query(dao.User).filter(dao.User.username == workspace_info.user).first()
            workspace = session.query(Workspace).filter(Workspace.user_id == user.id, Workspace.title == workspace_info.title).first()

            if workspace is not None:
                insert_status = False
                return insert_status

            # TODO: ADD WORKSPACE TO ALL USERS, YOU ARE RESTRICTING WORKSPACE NAME TO ONLY ONE USER...
            workspace = Workspace(
                title=workspace_info.title,
                desc=workspace_info.description,
                url=workspace_info.url,
                slug = workspace_info.slug,
                user_id=user.id,
            )
            session.add(workspace)
            session.commit()

            insert_status = True

        return insert_status

    def delete_workspace(self, username: str, workspace_name: str):
        is_deleted = False
        with Session(engine) as session:
            user = session.query(dao.User).filter(dao.User.username == username).first()
            print(session.query(Workspace).where(Workspace.user_id == user.id, Workspace.slug == workspace_name).first())
            session.query(Workspace).where(Workspace.user_id == user.id, Workspace.slug == workspace_name).delete()
            session.commit()
            is_deleted = True

        return is_deleted

    def get_all_workspaces(self, username: str):
        with Session(engine) as session:
            user = session.query(dao.User).filter(dao.User.username == username).first()
            workspaces = session.query(Workspace).where(Workspace.user_id == user.id ).order_by(Workspace.updated_at.desc()).all()

        return workspaces
