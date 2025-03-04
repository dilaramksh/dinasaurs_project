from django.shortcuts import render
from django.shortcuts import get_object_or_404
from social_media.models import Society, Membership, Event


#@login_required
def society_mainpage(request, society_id):
    """Display the webpage for a specific society."""
    society = get_object_or_404(Society, pk=society_id)

    #Maybe add as a separate getter function to helper? can be used in other places
    committee_members = [membership.user for 
                         membership in Membership.objects.filter(society=society) 
                         if membership.is_committee_member()]
    
    society_events = Event.objects.filter(society=society)

    is_committee_member = request.user in committee_members

    society_colour1 = society.colour1
    society_colour2 = society.colour2

    #Pass society colours

    context = {
        'society': society,
        'committee_members': committee_members,
        'society_events': society_events,
        'society_colour1': society_colour1,
        'society_colour2': society_colour2,
        'is_committee_member': is_committee_member,

    }

    return render(request, 'society/society_mainpage.html', context)


