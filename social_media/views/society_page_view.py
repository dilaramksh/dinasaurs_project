from django.shortcuts import render
from django.shortcuts import get_object_or_404
from social_media.models import Society, Membership, Event
from social_media.models.colour_history import SocietyColorHistory
from social_media.models.society_role import SocietyRole
from django.utils import timezone
from django.http import JsonResponse


#@login_required
def society_mainpage(request, society_id):
    """Display the webpage for a specific society and allow users to join."""
    society = get_object_or_404(Society, pk=society_id)

    # Retrieve committee members
    committee_members = [membership.user for 
                         membership in Membership.objects.filter(society=society) 
                         if membership.is_committee_member()]
    
    # Fetch upcoming events
    society_events = society.event_set.filter(date__gte=timezone.now()).order_by('date')
    
    # Retrieve past color changes
    past_colors = SocietyColorHistory.objects.filter(society=society).order_by('-updated_at')
    
    # Check if the current user is a committee member
    is_committee_member = request.user in committee_members

    # Fetch society colors
    society_colour1 = society.colour1
    society_colour2 = society.colour2

    context = {
        'society': society,
        'committee_members': committee_members,
        'society_events': society_events,
        'society_colour1': society_colour1,
        'society_colour2': society_colour2,
        'is_committee_member': is_committee_member,
        'past_colors': past_colors,
    }

    return render(request, 'society/society_mainpage.html', context)

def get_latest_society_colors(request, society_id):
    society = Society.objects.get(pk=society_id)
    latest_color = SocietyColorHistory.objects.filter(society=society).order_by('-updated_at').first()

    return JsonResponse({
        "colour1": latest_color.colour1 if latest_color else society.colour1,
        "colour2": latest_color.colour2 if latest_color else society.colour2
    })