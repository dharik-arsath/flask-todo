from flask import g, redirect
from flask import make_response, render_template, Response, request, jsonify

from app.dto.todo import TodoInfo
from app.todo.models import TodoModel
from . import todo_bp

todo_model = TodoModel()


@todo_bp.route("/")
@todo_bp.route("/workspaces")
def workspace():
    if g.is_logged_in is False:
        return redirect("/signin")


@todo_bp.route("/list-available-todo")
def list_todo():
    if g.is_logged_in is False:
        return redirect("/signin")

    username: str = request.cookies.get("username")
    if username == "":
        return redirect("/signin")

    all_todo = todo_model.fetch_completed_todo(username)
    return render_template("list.html", all_todo = all_todo)


@todo_bp.route("/list-completed-todo")
def list_completed_todo():
    if g.is_logged_in is False:
        return redirect("/signin")

    username: str = request.cookies.get("username")
    if username == "":
        return redirect("/signin")

    all_todo = todo_model.fetch_incomplete_todo(username)
    return render_template("completed.html", all_todo = all_todo)


@todo_bp.route("/completed", methods = ["POST"])
def update_completed_todo():
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int    = request.json.get("todo_id")
    is_updated      = todo_model.update_completed(update_status=True, todo_id = todo_id)

    resp = make_response(jsonify({
        "todo_id" : todo_id
    }))

    return resp


@todo_bp.route("/incompleted", methods=["POST"])
def incompleted_todo():
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int    = request.json.get("todo_id")
    is_updated      = todo_model.update_completed(update_status=False, todo_id = todo_id)

    resp = make_response(jsonify({
        "todo_id" : todo_id
    }))

    return resp



@todo_bp.route("/create-todo", methods = ["POST"])
def create_todo() -> Response:
    if g.is_logged_in is False:
        return redirect("/signin")

    title = request.form.get("title")
    desc  = request.form.get("desc")

    if not isinstance(title, str):
        raise TypeError("title must be instance of string...")
    elif not isinstance(desc, str):
        raise TypeError("description must be instance of string...")

    todo_info = TodoInfo( title = title, description = desc )

    insert_status = todo_model.create_todo(todo_info)
    if insert_status is True:
        status = 200
    else:
        status = 500

    print(status)
    resp = make_response(jsonify({
        "status" : status
    }))

    return resp


@todo_bp.route("/delete-todo", methods=["POST"])
def delete_todo():
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int = request.json.get("todo_id")
    if not isinstance(todo_id, int):
        raise TypeError(f"Invalid Data {todo_id}")

    todo_model.delete_todo(todo_id)
    resp  = make_response(jsonify({"todo_id" : todo_id}))
    return resp