from flask import Flask
from app.base.main import get_engine, Base
import os
import time

engine = get_engine()

def create_app():
    app = Flask(__name__)
    app.secret_key = "iporombamukkiyamidhu@121212"
    from app.todo import todo_bp
    from app.user import users_bp

    Base.metadata.create_all(engine)
    app.register_blueprint(todo_bp)
    app.register_blueprint(users_bp)

    os.environ["TZ"] = "Asia/Kolkata"
    time.tzset()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)