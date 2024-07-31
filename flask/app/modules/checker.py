from flask import session
from zenora import APIClient

from ..game_config import ADMINS
from ..core import core


def is_admin() -> bool:
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        _, output = core.check_player(current_user.username)
        return output or current_user.username in ADMINS
    else:
        return False
    
    
def is_player() -> bool:
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        output, _ = core.check_player(current_user.username)
        return output is not None
    else:
        return False
    

def is_game_admin() -> bool:
    if "token" in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return current_user.username in ADMINS
    else:
        return False