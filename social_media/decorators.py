from functools import wraps
from django.shortcuts import render


def user_type_required(user_type):
    def decorator(view_function):
        @wraps(view_function)
        def _wrapped_view(request, *view_args, **view_kwargs):
            print("User: ", request.user, request.user.user_type)
            if getattr(request.user, 'user_type', None) == user_type:
                return view_function(request, *view_args, **view_kwargs)
            return render(request, 'unauthorized_page.html')
        return _wrapped_view
    return decorator

