from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership
from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ValidationError

@login_required
def view_memberships(request):
    """
    Display all approved society memberships for the currently logged-in student.
    """
    memberships = Membership.objects.filter(user=request.user, society_role__society__status="approved")  
    print(memberships)
    return render(request, 'student/memberships.html', {'memberships': memberships})
    
@login_required
def remove_membership(request, membership_id):
    """
    Remove a membership for the currently logged-in student.
    """
    if request.method != "POST": 
        return JsonResponse({"success": False, "error": "Only POST requests are allowed."}, status=400)

    membership = get_object_or_404(Membership, id=membership_id, user=request.user)
    society_name = membership.society.name  
    membership.delete()  

    return JsonResponse({
        "success": True,
        "society_name": society_name,
        "message": f"You have successfully left {society_name}."
    })