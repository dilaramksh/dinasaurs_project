
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from social_media.decorators import user_type_required
from social_media.models import *
from django.shortcuts import render, get_object_or_404


#@user_type_required('student')
def dashboard(request):
    student = request.user
    memberships = Membership.objects.filter(user=student)

    user_societies = []
    for membership in memberships:
        society = membership.society_role.society
        role_name = membership.society_role.role_name
        user_societies.append({
            'society': society,
            'role': role_name
        })
    
    events = Event.objects.filter(society__in=[membership.society_role.society for membership in memberships])

    return render(request, 'student/student_dashboard.html', {
        'student': student,
        'user_societies': user_societies,
        'user_events': events,
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
        committee_members = [
            membership.user for membership in Membership.objects.filter(society_role__society=selected_society)
            if membership.is_committee_member()
        ]
    else:
        society_roles = SocietyRole.objects.filter(society__in=user_societies)

        committee_members = [
            membership.user for membership in Membership.objects.filter(society_role__society__in=user_societies)
            if membership.is_committee_member()
        ]

    return render(request, 'student/student_societies.html', {
        'student': student,
        'user_societies': user_societies,
        'selected_society': selected_society,
        'society_roles': society_roles,
        'committee_members': committee_members,  
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

