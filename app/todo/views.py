from flask import g, redirect
from flask import make_response, render_template, Response, request, jsonify

from app.dto.todo import TodoInfo, WorkspaceInfo
from app.todo.models import TodoModel, WorkspaceModel
from . import todo_bp

todo_model = TodoModel()
workspace_model = WorkspaceModel()


@todo_bp.route("/")
@todo_bp.route("/workspaces/", methods=["GET"])
def workspace():
    if g.is_logged_in is False:
        return redirect("/signin")

    username: str = request.cookies.get("username")
    workspaces = workspace_model.get_all_workspaces(username)

    return render_template("workspaces.html", workspaces = workspaces)

@todo_bp.route("/create-workspace", methods=["POST"])
def create_workspace():
    title: str = request.form.get("title")
    desc: str = request.form.get("desc")

    url       = f"/workspaces/{title}/list-available-todo"
    username: str = request.cookies.get("username")

    workspace = WorkspaceInfo(user=username, title=title, description=desc, url=url)
    model = WorkspaceModel()
    is_added = model.add_workspace(workspace)

    if is_added:
        status_code = 200
    else:
        status_code = 500

    resp = make_response({
        "status": status_code
    })

    return resp

@todo_bp.route("/delete-workspace", methods=["POST"])
def delete_workspace():
    workspace: str = request.form.get("workspace")
    model = WorkspaceModel()

    username: str = request.cookies.get("username")
    is_deleted = model.delete_workspace(username=username, workspace_name=workspace)

    if is_deleted:
        status_code = 200
    else:
        status_code = 500

    resp = make_response({
        "status": status_code
    })

    return resp


@todo_bp.route("/workspaces/<string:workspace_name>/list-available-todo")
def list_todo(workspace_name: str):
    if g.is_logged_in is False:
        return redirect("/signin")

    username: str = request.cookies.get("username")
    if username == "":
        return redirect("/signin")

    all_todo = todo_model.fetch_completed_todo(username, workspace_name)
    return render_template("list.html", all_todo = all_todo)


@todo_bp.route("/workspaces/<string:workspace_name>/list-completed-todo")
def list_completed_todo(workspace_name: str):
    if g.is_logged_in is False:
        return redirect("/signin")

    username: str = request.cookies.get("username")
    if username == "":
        return redirect("/signin")

    all_todo = todo_model.fetch_incomplete_todo(username, workspace_name)
    return render_template("completed.html", all_todo = all_todo)


@todo_bp.route("/workspaces/<string:workspace_name>/completed", methods = ["POST"])
def update_completed_todo(workspace_name: str):
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int    = request.json.get("todo_id")
    is_updated      = todo_model.update_completed(update_status=True, todo_id = todo_id)

    resp = make_response(jsonify({
        "todo_id" : todo_id
    }))

    return resp


@todo_bp.route("/workspaces/<string:workspace_name>/incompleted", methods=["POST"])
def incompleted_todo(workspace_name: str):
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int    = request.json.get("todo_id")
    is_updated      = todo_model.update_completed(update_status=False, todo_id = todo_id    )

    resp = make_response(jsonify({
        "todo_id" : todo_id
    }))

    return resp



@todo_bp.route("/workspaces/<string:workspace_name>/create-todo", methods = ["POST"])
def create_todo(workspace_name: str) -> Response:
    if g.is_logged_in is False:
        return redirect("/signin")

    title = request.form.get("title")
    desc  = request.form.get("desc")

    todo_info = TodoInfo( title = title, description = desc, workspace=workspace_name )

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


@todo_bp.route("/workspaces/<string:workspace_name>/delete-todo", methods=["POST"])
def delete_todo(workspace_name: str):
    if g.is_logged_in is False:
        return redirect("/signin")

    todo_id: int = request.json.get("todo_id")
    if not isinstance(todo_id, int):
        raise TypeError(f"Invalid Data {todo_id}")

    todo_model.delete_todo(todo_id, workspace_name)
    resp  = make_response(jsonify({"todo_id" : todo_id}))
    return resp
