from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.todo import todo_bp
    from app.user import users_bp

    app.register_blueprint(todo_bp)
    app.register_blueprint(users_bp)

    return app
