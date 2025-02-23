
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from social_media.models import Society, Membership
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    user_type = current_user.user_type

    if user_type == 'student':
        committee_societies = Society.objects.filter(
            membership__user=current_user
        ).exclude(
            membership__society_role__role_name__in=["member", "standard member"] 
        ).distinct()
    else:
        committee_societies = None

    context = {
        'user': current_user,
        'committee_societies': committee_societies,
    }
    if user_type == "student":
        template = "student/student_dashboard.html"
    else:
        template = 'student/student_dashboard.html'
    
    return render(request, template, context)


#@login_required
def get_society_dashboard(request, society_id):
    """Display the dashboard for a specific society."""
    society = get_object_or_404(Society, pk=society_id)
    return render(request, 'society/society_dashboard.html', {'society': society})