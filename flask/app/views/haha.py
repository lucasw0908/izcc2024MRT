import logging
from flask import Blueprint, redirect

from ..modules.checker import is_game_admin


log = logging.getLogger(__name__)
haha = Blueprint("haha", __name__)


@haha.route("/wtf")
def wtf():
    if not is_game_admin():
        return redirect("/")
    return "OwO"


@haha.route("/rickroll")
def rickroll():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")