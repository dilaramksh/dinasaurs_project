
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from social_media.decorators import user_type_required
from social_media.models import *


#@user_type_required('student')
@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    student = request.user

    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    user_events = Event.objects.filter(society__in=user_societies)

    return render(request, 'student/student_dashboard.html', {
        'student': student,
        'user_societies': user_societies,
        'user_events': user_events,
    })