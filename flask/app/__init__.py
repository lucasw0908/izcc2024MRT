import os
import logging
import logging.handlers
from flask import Flask
from flask_cors import CORS
from flask.logging import default_handler
from flask_wtf import CSRFProtect

from .config import DevConfig, ProdConfig, BASEDIR
from .models import db
from .modules.socketio import socketio
from .core import core


log = logging.getLogger(__name__)


def init_logger(debug: bool=False) -> None:
    """
    Initialize the logger.
    
    Parameters
    ----------
    debug: :type:`bool`
        If debug is true, the logger will log all messages.
    """
        
    formatter = logging.Formatter("[{asctime}] {levelname} {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{")
    
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
        
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(BASEDIR, "logs", "app.log"),
        encoding="utf-8",
        maxBytes=8**7, 
        backupCount=8
    )
        
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)
    
    #logging.getLogger().addHandler(default_handler)
    
def app_load_blueprints(app: Flask) -> None:
    """
    Load all blueprints
    
    Parameters
    ----------
    app: :class:`Flask`
        The flask app.
    """
    
    from .views.account_sys import account_sys
    from .views.admin_api import admin_api
    from .views.api import api
    from .views.error_handler import error_handler
    from .views.main import main
    from .views.haha import haha
    
    app.register_blueprint(account_sys)
    app.register_blueprint(admin_api)
    app.register_blueprint(api)
    app.register_blueprint(error_handler)
    app.register_blueprint(main)
    app.register_blueprint(haha)
    
    
def create_app() -> Flask:
    """
    Initialize the app.
    
    Returns
    -------
    app: :class:`Flask`
        A flask app.
    """
    init_logger(debug=True)
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    csrf = CSRFProtect(app)
    CORS(app)
    app_load_blueprints(app)
    db.__init__(app)
    socketio.init_app(app, cors_allowed_origins="*")
    core.init_socketio(socketio)
    with app.app_context(): db.create_all()
    
    return app