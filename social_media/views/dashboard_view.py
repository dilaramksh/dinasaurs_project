
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    user_type = current_user.user_type

    context = {
        'user': current_user,
    }

    if user_type == 'Univeristy Admin':
        #context.update(admin_dashboard_context(request, current_user))
        template = 'admin_dashboard.html'
    elif user_type == 'Society':
        template = 'society_dashboard.html'
    else:
        template = 'student_dashboard.html'
    
    return render(request, template, context)