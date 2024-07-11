import logging
from flask import Blueprint, Response, render_template, redirect, send_file, session 

from ..core import core
from ..modules.socketio import socketio


log = logging.getLogger(__name__)


socketio.on("connect")
def connect():
    log.info("Client connected")
    socketio.emit("connected", {"data": "Connected"})