from flask import make_response, render_template, Response, request, jsonify
from sqlalchemy.orm import Session

from app.data_models.todo import Todo
from app.data_models.todo import get_engine
from . import todo_bp

engine = get_engine()


@todo_bp.route("/list-available-todo")
def list_todo():
    with Session(engine) as session:
        all_todo = session.query(Todo).filter(Todo.is_completed == False).order_by(Todo.created_at.desc())

    return render_template("list.html", all_todo = all_todo)


@todo_bp.route("/list-completed-todo")
def list_completed_todo():
    with Session(engine) as session:
        all_todo = session.query(Todo).filter(Todo.is_completed == True).order_by(Todo.created_at.desc())

    return render_template("completed.html", all_todo = all_todo)


@todo_bp.route("/completed", methods = ["POST"])
def completed_todo():
    todo_id: str    = request.json.get("todo_id")
    with Session(engine) as session:
        todo = session.query(Todo).where(Todo.id == int( todo_id )).first()
        todo.is_completed = True

        session.commit()

    resp = make_response(jsonify({
        "todo_id" : int(todo_id)
    }))
    return resp


@todo_bp.route("/create-todo", methods = ["POST"])
def create_todo() -> Response:
    with Session(engine) as session:
        todo = Todo(
            title = request.form.get("title"),
            desc  = request.form.get("desc")
        )

        session.add(todo)

        session.commit()

    resp = make_response(jsonify({
        "status" : 200
    }))
    return resp


@todo_bp.route("/delete-todo", methods=["POST"])
def delete_todo():
    todo_id: str = request.json.get("todo_id")
    with Session(engine) as session:
        session.query(Todo).where(Todo.id == todo_id).delete()
        session.commit()
    resp  = make_response(jsonify({"todo_id" : todo_id}))
    return resp