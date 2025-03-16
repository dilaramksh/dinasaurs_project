from django.shortcuts import render
from social_media.models import Membership
from django.contrib.auth.decorators import login_required

@login_required
def view_memberships(request):
    """Display all memberships of a student user"""
    memberships = Membership.objects.filter(user=request.user)  
    print(memberships)
    return render(request, 'student/memberships.html', {'memberships': memberships})