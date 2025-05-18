from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario' not in request.session:
            return redirect('Login')
        return view_func(request, *args, **kwargs)
    return wrapper
