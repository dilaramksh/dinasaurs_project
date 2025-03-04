from django.conf import settings
from django.shortcuts import redirect
from social_media.models import *


def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function


def redirect_to_society_dashboard(request, fallback='dashboard'):
    """Redirects to the correct society dashboard or falls back to the general dashboard."""
    society_id = request.session.get('active_society_id')
    if society_id:
        return redirect('society_dashboard', society_id=society_id)
    return redirect(fallback)
