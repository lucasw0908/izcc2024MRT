import logging
from flask import Blueprint, Response, render_template


log = logging.getLogger(__name__)
main = Blueprint("main", __name__)


@main.after_request
def checking(response: Response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "deny"
    return response
    

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/test")
def test():
    return render_template("test.html")