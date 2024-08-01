import logging
from flask_socketio import SocketIO

from ..core import core


log = logging.getLogger(__name__)
socketio = SocketIO()


@socketio.on("connect")
def connect():
    log.info("Client connected")
    socketio.emit("connected", {"data": "Connected"})