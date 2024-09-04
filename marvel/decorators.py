from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_rols=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_rols:
                return view_func(request, *args, **kwargs)
            
            else:
                return HttpResponse('You are not authorized to view this page')
            
        return wrapper_func
    return decorators


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group =None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('/')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_function