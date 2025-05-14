from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario' not in request.session:
            return redirect('Login')
        return view_func(request, *args, **kwargs)
    return wrapper