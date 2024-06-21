import logging
from flask import Blueprint, Response, render_template
from ..core import Core


log = logging.getLogger(__name__)
test = Blueprint("test", __name__)


@test.route("/test")
def print_data():
    test_core = Core()
    log.debug("Print data.")
    return "None"