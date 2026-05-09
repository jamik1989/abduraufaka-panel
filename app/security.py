from functools import wraps
from typing import Callable

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.config import settings


def is_logged_in(request: Request) -> bool:
    return bool(request.session.get("admin_logged_in"))


def require_login(handler: Callable):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request is None:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if request is None or not is_logged_in(request):
            return RedirectResponse(url="/login", status_code=303)
        return await handler(*args, **kwargs)

    return wrapper


def check_admin_login(username: str, password: str) -> bool:
    return username == settings.admin_username and password == settings.admin_password
