from flask import Blueprint

todo_bp = Blueprint("todo", __name__)

from . import views
