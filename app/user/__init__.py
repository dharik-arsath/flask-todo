from flask import Blueprint

users_bp = Blueprint("user", __name__)

from . import user_views
