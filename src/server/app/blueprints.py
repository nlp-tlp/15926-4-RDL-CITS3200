from flask import Blueprint

main = Blueprint("main", __name__)
ctrl = Blueprint("ctrl", __name__)

from app import routes
