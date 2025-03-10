from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms import CustomisationForm, PostForm, EventCreationForm
from social_media.models.colour_history import SocietyColorHistory
from social_media.models import Society, Event, Membership, EventsParticipant
from django.utils.timezone import now
from datetime import date
from django.http import JsonResponse
from social_media.helpers import redirect_to_society_dashboard 



def event_creation(request, society_id):

    society = get_object_or_404(Society, pk=society_id)
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.society = society
            event.save()
            messages.success(request, "Your event has been created.")
            return redirect_to_society_dashboard(request)
        else:                  
            messages.error(request, "There was an error with your submission. Please try again.")
    
    else:
        form = EventCreationForm()

    return render(request, 'society/event_creation.html', {'form': form})

def terminate_society(request, society_id):
    society = get_object_or_404(Society, pk=society_id)  

    if request.method == "POST":
        society.delete()
        request.session.pop('active_society_id', None)
        return redirect("dashboard")  
    
    return render(request, "society/terminate_society.html")


def view_members(request, society_id):
 
    memberships = Membership.objects.filter(society_id=society_id).select_related('user', 'society_role')
    committee_members = [m.user for m in memberships if m.society_role.is_committee_role()]
    
    all_users = list(set(m.user for m in memberships))

    context = {
        "committee_members": committee_members,
        "users": all_users,  
    }
    
    return render(request, "society/view_members.html", context)

def view_upcoming_events(request, society_id):
    society = get_object_or_404(Society, pk=society_id)
    events = Event.objects.filter(date__gte=date.today()).order_by("date")
    return render(request, 'society/view_upcoming_events.html', {'events': events})

def event_details(request, event_id):
    """Return event details as JSON for the modal popup."""
    event = get_object_or_404(Event, pk=event_id)
    participants = EventsParticipant.objects.filter(event=event).select_related("membership")

    data = {
        "name": event.name,
        "date": event.date.strftime("%Y-%m-%d"),
        "location": event.location,
        "description": event.description,
        "participants": [p.membership.user.username for p in participants],
    }
    
    return JsonResponse(data)

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user  
            post.save()
            messages.success(request, "Post created successfully!")  
            return redirect_to_society_dashboard(request)
        else:
            messages.error(request, "Error in post creation. Please check the form.")
        
    else:
        form = PostForm()

    return render(request, 'society/create_post.html', {"form": form})

def customise_society_view(request, society_id):
    society = get_object_or_404(Society, pk=society_id)

    if request.method == 'POST':
        form = CustomisationForm(request.POST, instance=society)
        if form.is_valid():
            # Save the previous colors in history
            SocietyColorHistory.objects.create(
                society=society,
                previous_colour1=society.colour1,
                previous_colour2=society.colour2
            )

            # Save the new color values
            form.save()
            return redirect('society_mainpage', society_id=society.id)
    else:
        form = CustomisationForm(instance=society)

    return render(request, 'society/customise_society.html', {'form': form, 'society': society})


def update_society_colors(request, society_id):

    society = get_object_or_404(Society, pk=society_id)

    if request.method == "POST":
        new_colour1 = request.POST.get("colour1")
        new_colour2 = request.POST.get("colour2")

        if society.colour1 != new_colour1 or society.colour2 != new_colour2:
            SocietyColorHistory.objects.create(
                society=society,
                previous_colour1=society.colour1,
                previous_colour2=society.colour2
            )

 
        society.colour1 = new_colour1
        society.colour2 = new_colour2
        society.save()


        return redirect('society/society_mainpage', society_id=society.id)  

    return render(request, 'society/society_mainpage.html', {'society': society})
