import logging
from logging import Logger

from flask import render_template, request, redirect, make_response

from . import users_bp
from .models import UserModel, UserInfo

user_model = UserModel()
# user_info  = UserInfo()
log         = Logger("auth_logger")
log.level   = logging.INFO


@users_bp.route("/")
@users_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")

    username: str = request.form.get("username")
    password: str = request.form.get("password")

    print("-------------------------------------------------------------------")
    print(username, password)
    try:
        if not isinstance(username, str):
            raise TypeError("Invalid username...")
        if not isinstance(password, str):
            raise TypeError("Invalid Password...")
    except TypeError:
        return redirect(request.url)

    user_info = UserInfo(
        username = username,
        password = password
    )
    is_valid_credential = user_model.validate_user(user_info)

    resp = make_response()
    if is_valid_credential:
        resp.set_cookie("username", username)
        return redirect("/list-available-todo")
    else:
        # resp.status_code = 401
        return redirect("/signin")


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username: str = request.form.get("username")
    password: str = request.form.get("password")
    if not isinstance(username, str):
        raise TypeError(f"username must be instance of str, got {username}")

    if not isinstance(password, str):
        raise TypeError(f"password must be instance of str")

    user_info = UserInfo(
        username = username,
        password = password
    )

    user_model.create_new_user(user_info)
    return redirect("/signin")


@users_bp.route("/signout", methods=["GET"])
def signout():
    resp = make_response()
    resp.set_cookie("username", "", expires=0)

    return redirect("/signin")