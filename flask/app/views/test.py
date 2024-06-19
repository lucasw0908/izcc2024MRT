import logging
from flask import Blueprint, Response, render_template
from ..core import TestCore


log = logging.getLogger(__name__)
test = Blueprint("test", __name__)


@test.route("/test")
def print_data():
    test_core = TestCore()
    print(".")
    log.debug("Print data.")
    return test_core.print_data()