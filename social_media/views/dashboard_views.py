
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from social_media.models import Society, Membership, Event, SocietyRole
from django.shortcuts import get_object_or_404
from social_media.models import Society
from social_media.helpers import membership_required
from django.http import JsonResponse

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    user_type = current_user.user_type

    active_society_id = request.session.get('active_society_id')
    if active_society_id:
        return redirect('society_dashboard', society_id=active_society_id)
    
    context = {
        'user': current_user,
    }

    if user_type == "student":
        memberships = Membership.objects.filter(user=current_user)
        user_societies = [membership.society_role.society for membership in memberships]
        user_events = Event.objects.filter(society__in=user_societies)
        society_roles = SocietyRole.objects.filter(society__in=user_societies)

        committee_societies = Society.objects.filter(
            membership__user=current_user
        ).exclude(
            membership__society_role__role_name__in=["member", "standard member"] 
        ).distinct()

        context = {
            'user': current_user,
            'user_societies': user_societies,
            'user_events': user_events,
            'society_roles': society_roles,
            'committee_societies': committee_societies,
        }

        template = "student/student_dashboard.html"
    elif user_type == 'uni_admin':
        status_filter = request.GET.get("status", "pending")


        if status_filter not in ["pending", "approved", "blocked"]:
           status_filter = "pending"  # fallback


        # Filter societies by chosen status and founder's university = admin's university
        societies = Society.objects.filter(
            status=status_filter,
            founder__university=request.user.university
        ).order_by("name") # temp
        
        context = {
            "societies": societies,
            "chosen_status": status_filter
        }
        template = "uni_admin/uni_admin_dashboard.html"
    else:
        template = 'student/student_dashboard.html' # ???
    
    return render(request, template, context)


@login_required
@membership_required
def get_society_dashboard(request, society_id):
    """Display the dashboard for a specific society."""
    society = get_object_or_404(Society, pk=society_id)

    # Store the selected society ID
    request.session['active_society_id'] = society.id
    
    return render(request, 'society/society_dashboard.html', {'society': society})

@login_required
def get_student_dashboard(request):
    """Clears the active society and redirects to the student dashboard."""
    request.session.pop('active_society_id', None) 
    return redirect('dashboard')


@login_required
def dashboard_from_mainpage(request, society_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)
    
    society = get_object_or_404(Society, id=society_id)
    
    # Check if user is already a member
    if Membership.objects.filter(user=request.user, society=society).exists():
        return JsonResponse({'success': False, 'error': 'You are already a member of this society'}, status=400)

    # Assuming there's a default role for new members (e.g., standard member)
    default_role = SocietyRole.objects.get(role_name="Member")  # Adjust based on your actual roles

    # Create membership
    Membership.objects.create(user=request.user, society=society, society_role=default_role)

    return JsonResponse({'success': True})
