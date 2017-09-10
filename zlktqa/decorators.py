# Author:Clin
from flask import session,redirect,url_for
from functools import wraps


def login_required(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get('userid'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wapper
