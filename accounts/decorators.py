from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to view this resource")

        return wrapper_func

    return decorators


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            list = request.user.groups.all()
            print("groups: ", list)
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user')
        elif group == 'admins':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Your don't have permission please contact admin")
    return wrapper_func
def is_admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            list = request.user.groups.all()
            print("groups: ", list)
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user')
        elif group == 'admins':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Your don't have permission please contact admin")
    return wrapper_func
def is_user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            list = request.user.groups.all()
            print("groups: ", list)
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user')
        elif group == 'admins':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Your don't have permission please contact admin")
    return wrapper_func
def is_manager_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            list = request.user.groups.all()
            print("groups: ", list)
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user')
        elif group == 'admins':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Your don't have permission please contact admin")
    return wrapper_func
def belongs_to_group(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            list = request.user.groups.all()
            print("groups: ", list)
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user')
        elif group == 'admins':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Your don't have permission please contact admin")
    return wrapper_func
