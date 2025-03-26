from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from social_media.models import *
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


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

def committee_required(view_function):
    """Decorator for views that checks if a user is a committee member of the society."""

    def modified_view_function(request, society_id, *args, **kwargs):
        society = get_object_or_404(Society, pk=society_id)
        memberships = Membership.objects.filter(user=request.user, society=society).annotate(
            is_committee=ExpressionWrapper(
                ~Q(society_role__role_name__iexact="member") &
                ~Q(society_role__role_name__iexact="standard member"),
                output_field=BooleanField()
            )
        )
        if not memberships.filter(is_committee=True).exists():
            raise PermissionDenied

        return view_function(request, society_id, *args, **kwargs)

    return modified_view_function

"""
Helpers
"""
def get_committee_members(society):
    """Retrieve committee members for a given society."""
    return [membership.user for membership in Membership.objects.filter(society=society) if membership.is_committee_member()]

def is_user_committee(user, society):
    """Check if user is in the committee of a society."""
    user_membership = Membership.objects.filter(user=user, society=society).first()
    if not user_membership:
        return False
    if user_membership.is_committee_member():
        return True
    return False
    

def redirect_to_society_dashboard(request, fallback='dashboard'):
    """Redirects to the correct society dashboard or falls back to the general dashboard."""
    society_id = request.session.get('active_society_id')
    if society_id:
        return redirect('society_dashboard', society_id=society_id)
    return redirect(fallback)
