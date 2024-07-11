import logging
from flask import Blueprint, render_template


log = logging.getLogger(__name__)
error_handler = Blueprint("error_handler", __name__)


@error_handler.app_errorhandler(403)
def error403(error):
    return render_template("error/403.html", error=error), 403


@error_handler.app_errorhandler(404)
def error404(error):
    return render_template("error/404.html", error=error), 404


@error_handler.app_errorhandler(500)
def error500(error):
    log.error(error)
    return render_template("error/500.html", error=error), 500


@error_handler.on_error_default
def default_error_handler(error):
    log.error(error)