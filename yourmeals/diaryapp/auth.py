from functools import wraps
import base64
import hashlib
import hmac
import os

from django.http import HttpResponseRedirect
from dotenv import load_dotenv

from . import MainContr

MainContr = MainContr()

load_dotenv()

SECRET_USERMAIL_SALT = os.getenv("SECRET_USERMAIL_SALT")

def sign_data(data: str):
    """
    Return signed data
    """
    return hmac.new(
        SECRET_USERMAIL_SALT.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_email_from_signed_data(signed_data: str):
    email, sign = signed_data.split(".")
    email = base64.b64decode(email.encode()).decode()
    valid_sign = sign_data(email)
    if hmac.compare_digest(valid_sign, sign):
        return email


def read_usermail_cookies(request):
    email_cookie = request.COOKIES.get('email', None)
    if not email_cookie:
        return None
    valid_email = get_email_from_signed_data(email_cookie)
    return valid_email


def authorize(f):
    @wraps(f)
    def decorated_function(request, *args, **kws):
        USER_MAIL = read_usermail_cookies(request)
        if USER_MAIL is None or not MainContr.get_user(USER_MAIL): 
            return HttpResponseRedirect('/login/')
        return f(request, *args, **kws)  
    return decorated_function