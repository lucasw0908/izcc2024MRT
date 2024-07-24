import logging
from flask import Blueprint, render_template


log = logging.getLogger(__name__)
error_handler = Blueprint("error_handler", __name__)


@error_handler.app_errorhandler(403)
def error403(error):
    return render_template("error.html", error=str(error).split(".")[:-1], error_code="403"), 403


@error_handler.app_errorhandler(404)
def error404(error):
    return render_template("error.html", error=str(error).split(".")[:-1], error_code="404"), 404


@error_handler.app_errorhandler(500)
def error500(error):
    log.error(error)
    return render_template("error.html", error=str(error).split(".")[:-1], error_code="500"), 500