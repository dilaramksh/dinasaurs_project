from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership
from django.shortcuts import render
from django.contrib import messages

@login_required
def view_memberships(request):
    """
    Display all approved society memberships for the currently logged-in student.

    This view retrieves all memberships for the current user where the society status is approved
    and renders them on the memberships page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered memberships page with the user's memberships.
    """
    memberships = Membership.objects.filter(user=request.user, society_role__society__status="approved")  
    print(memberships)
    return render(request, 'student/memberships.html', {'memberships': memberships})
    
@login_required
def remove_membership(request, membership_id):
    """
    Remove a membership for the currently logged-in student.

    This view handles the removal of a membership for the current user. It only allows removal through
    a POST request to prevent accidental deletion.

    Args:
        request (HttpRequest): The request object.
        membership_id (int): The ID of the membership to be removed.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
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