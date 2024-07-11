import os
import json
import logging

from ..config import BASEDIR


log = logging.getLogger(__name__)


def load_data(filename: str) -> dict:
    
    if not os.path.exists(os.path.join(BASEDIR, "data", f"{filename}.json")):
        log.warning(f"File {filename}.json not found.")
        return {}
    
    with open(os.path.join(BASEDIR, "data", f"{filename}.json"), "r", encoding="utf-8") as file:
        return json.load(file)