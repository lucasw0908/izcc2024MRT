import logging
from flask_socketio import SocketIO


log = logging.getLogger(__name__)
socketio = SocketIO()

@socketio.on_error_default
def default_error_handler(error):
    log.error(error)