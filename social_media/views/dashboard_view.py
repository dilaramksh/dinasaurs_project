
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from social_media.decorators import user_type_required
from social_media.models import *
from django.shortcuts import render, get_object_or_404


#@user_type_required('student')
@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    student = request.user
    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    user_events = Event.objects.filter(society__in=user_societies)
    society_roles = SocietyRole.objects.filter(society__in=user_societies)

    return render(request, 'student/student_dashboard.html', {
        'student': student,
        'user_societies': user_societies,
        'user_events': user_events,
        'society_roles':society_roles,
    })



def student_societies(request):
    student = request.user
    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    selected_society = None

    if request.method == 'GET' and 'society_id' in request.GET:
        society_id = request.GET['society_id']
        selected_society = get_object_or_404(Society, id=society_id)
        if selected_society not in user_societies:
            selected_society = None

    if selected_society:
        society_roles = SocietyRole.objects.filter(society=selected_society)
    else:
        society_roles = SocietyRole.objects.filter(society__in=user_societies)

    return render(request, 'student/student_societies.html', {
        'student': student,
        'user_societies': user_societies,
        'selected_society': selected_society,
        'society_roles': society_roles
    })

def student_events(request):
    student = request.user
    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    user_events = Event.objects.filter(society__in=user_societies)

    return render(request, 'student/student_events.html', {
        'student': student,
        'user_societies': user_societies,
        'user_events': user_events,
    })

