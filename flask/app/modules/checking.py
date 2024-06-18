from flask import redirect, abort
from functools import wraps
from typing import Callable, Literal

from ..models.users import Users

def admin_checker(func: Callable, username: str, forbidden: Literal["raise_403_error", "redirect"], redirect_url: str="/") -> Callable:
    """
    Parameters
    ----------
    func: :type:`Callable`
        The function to decorate.
    username: :type:`str`
        The username to check.
    forbidden: :type:`Literal["raise_403_error", "redirect"]`
        If the user is not an admin, raise a 403 error or redirect to a page.
    redirect_url: :type:`str`
        The url to redirect to if forbidden is "redirect".
        
    Returns
    -------
    :type:`bool`
        True if the user is an admin, otherwise False.
    """
    def decorate(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = Users.query.filter_by(username=username, is_admin=True).first()
            if user is None:
                if forbidden == "redirect":
                    return redirect(redirect_url)
                elif forbidden == "raise_403_error": 
                    return abort(403)
                else:
                    raise ValueError("forbidden must be 'raise_403_error' or 'redirect'")
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorate