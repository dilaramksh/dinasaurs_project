from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from social_media.models import *

"""
Decorators
"""
def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def membership_required(view_function):
    """Decorator for views that checks if a user is a member of the society."""
    
    def modified_view_function(request, society_id, *args, **kwargs):
        society = get_object_or_404(Society, pk=society_id)
        if not Membership.objects.filter(user=request.user, society_role__society=society).exists():
            return redirect('dashboard')
        return view_function(request, society_id, *args, **kwargs)
    return modified_view_function

"""
Helpers
"""
def get_committee_members(society):
    """Retrieve committee members for a given society."""
    return [membership.user for membership in Membership.objects.filter(society=society) if membership.is_committee_member()]

def redirect_to_society_dashboard(request, fallback='dashboard'):
    """Redirects to the correct society dashboard or falls back to the general dashboard."""
    society_id = request.session.get('active_society_id')
    if society_id:
        return redirect('society_dashboard', society_id=society_id)
    return redirect(fallback)
