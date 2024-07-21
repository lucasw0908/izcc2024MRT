import logging
from flask import Blueprint, Response, render_template, jsonify

from ..core import core
from ..data import load_data


log = logging.getLogger(__name__)
test = Blueprint("test", __name__)


@test.route("/test")
def test_method():
    choice = core.move("admins", 6)
    log.debug(choice)
    return jsonify(choice)