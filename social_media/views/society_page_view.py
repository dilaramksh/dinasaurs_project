from django.shortcuts import render, get_object_or_404
from social_media.models import Society, Membership, Event
from social_media.models.colour_history import SocietyColorHistory
from social_media.models.post import Post
from django.utils import timezone
from django.http import JsonResponse

#@login_required
def society_mainpage(request, society_id):
    """
    Display the webpage for a specific society and allow users to join.

    This view retrieves the details of a specific society, including its committee members,
    upcoming events, past colors, and posts. It also checks if the current user is a member
    or a committee member of the society.

    Args:
        request (HttpRequest): The request object.
        society_id (int): The ID of the society.

    Returns:
        HttpResponse: The rendered society mainpage with the society details.
    """
    society = get_object_or_404(Society, pk=society_id)
    
    memberships = Membership.objects.filter(society_id=society_id).select_related('user', 'society_role')
    committee_members = [m.user for m in memberships if m.society_role.is_committee_role()]
    
    society_events = society.event_set.filter(date__gte=timezone.now()).order_by('date')
    
    past_colors = SocietyColorHistory.objects.filter(society=society).order_by('-updated_at')

    posts = society.posts.all().order_by('-created_at')
    is_committee_member = request.user in committee_members
    is_member = Membership.objects.filter(society=society, user=request.user).exists()

    society_colour1 = society.colour1
    society_colour2 = society.colour2

    context = {
        'society': society,
        'society_id': society_id,
        'committee_members': committee_members,
        'society_events': society_events,
        'posts': posts,
        'society_colour1': society_colour1,
        'society_colour2': society_colour2,
        'is_committee_member': is_committee_member,
        'is_member': is_member,
        'past_colors': past_colors,
    }

    return render(request, 'society/society_mainpage.html', context)


def get_latest_society_colors(request, society_id):
    """
    Get the latest colors of a specific society.

    This view retrieves the latest colors of a specific society from the color history.
    If no color history is found, it returns the current colors of the society.

    Args:
        request (HttpRequest): The request object.
        society_id (int): The ID of the society.

    Returns:
        JsonResponse: A JSON response containing the latest colors of the society.
    """
    society = get_object_or_404(Society, pk=society_id)
    latest_color = SocietyColorHistory.objects.filter(society=society).order_by('-updated_at').first()

    return JsonResponse({
        "colour1": latest_color.previous_colour1 if latest_color else society.colour1,
        "colour2": latest_color.previous_colour2 if latest_color else society.colour2
    })