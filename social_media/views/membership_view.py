from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership
from django.shortcuts import render


@login_required
def view_memberships(request):
    """Display all memberships of a student user"""
    memberships = Membership.objects.filter(user=request.user, society_role__society__status="approved")  
    print(memberships)
    return render(request, 'student/memberships.html', {'memberships': memberships})


@login_required
def join_society(request, society_id):
    """Allow a student to join a society"""
    society = get_object_or_404(Society, pk=society_id)
    
    # Check if the student is already a member
    if Membership.objects.filter(user=request.user, society=society).exists():
        return JsonResponse({'success': False, 'error': 'You are already a member of this society.'})
    
    # Otherwise, create a new membership (you can also set a default role here)
    try:
        Membership.objects.create(user=request.user, society=society, society_role=None)  # Adjust role if needed
        return JsonResponse({'success': True})
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': str(e)})
