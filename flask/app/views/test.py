import logging
from flask import Blueprint, Response, render_template, jsonify
from ..core import Core


log = logging.getLogger(__name__)
test = Blueprint("test", __name__)


@test.route("/test")
def print_data():
    core = Core()
    log.debug("Test...")
    print(core.move("大安森林公園"))
    print(core.metro.move("大坪林"))
    print(core.metro.move("新北產業園區"))
    #print(core.metro.graph)
    return jsonify(core.metro.graph)