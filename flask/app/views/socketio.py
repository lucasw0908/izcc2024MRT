import logging
from flask import Blueprint
from flask_socketio import SocketIO


log = logging.getLogger(__name__)
socketio = SocketIO()
socketio_bp = Blueprint("socketio_bp", __name__)

@socketio.on_error_default
def default_error_handler(error):
    log.error(error)