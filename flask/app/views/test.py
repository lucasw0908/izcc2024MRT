import logging
from flask import Blueprint, Response, render_template, jsonify

from ..core import Core
from ..data import load_data


log = logging.getLogger(__name__)
test = Blueprint("test", __name__)


@test.route("/test")
def print_data():
    return jsonify(load_data("api_data"))