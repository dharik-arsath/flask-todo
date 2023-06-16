from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = "iporombamukkiyamidhu@121212"
    from app.todo import todo_bp
    from app.user import users_bp

    app.register_blueprint(todo_bp)
    app.register_blueprint(users_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)