import logging
from logging import Logger

from flask import render_template, request, redirect, make_response, session, g

from . import users_bp
from .models import UserModel, UserInfo

user_model = UserModel()
# user_info  = UserInfo()
log         = Logger("auth_logger")
log.level   = logging.INFO

login_exempt_routes = [
    "/signin", "/signup"
]


def validate_cookie():
    cookie_username  = request.cookies.get("username")
    session_username = session.get("username")

    print(cookie_username, session_username)
    g.is_logged_in = False
    if cookie_username is not None and session_username is not None:
        print(f"checking {cookie_username == session_username}")
        if cookie_username == session_username:
            g.is_logged_in = True
            print(g.is_logged_in)
    else:
        g.is_logged_in = False
        print(g.is_logged_in)

@users_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")

    username: str = request.form.get("username")
    password: str = request.form.get("password")

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

    if is_valid_credential:
        resp = redirect("/workspaces")
        resp.set_cookie("username", username)
        session["username"] = username

        return resp
    else:
        # resp.status_code = 401
        return render_template("signin.html", username= username, failed_auth = True)


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
    if g.is_logged_in is False:
        return redirect("/signin")

    resp = make_response()
    resp.set_cookie("username", "", expires=0)
    session.pop("username")

    return redirect("/signin")
