import logging
from flask import Blueprint
from flask_socketio import SocketIO

from ..core import core


log = logging.getLogger(__name__)
socketio = SocketIO()
core.init_socketio(socketio)