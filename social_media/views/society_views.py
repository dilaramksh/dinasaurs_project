from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms import CustomisationForm, PostForm, EventCreationForm, TeamCreationForm
from social_media.models.colour_history import SocietyColorHistory
from social_media.models import Society, Event, Membership, EventsParticipant, Competition, Team, TeamMembership, CompetitionParticipant
from django.utils.timezone import now
from datetime import date
from django.http import JsonResponse
from social_media.helpers import redirect_to_society_dashboard 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from social_media.forms.competition_creation_form import CompetitionForm

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

def create_post(request, society_id):
    society = get_object_or_404(Society, id=society_id) 

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.society = society 
            post.save()
            messages.success(request, "Post created successfully!")  
            return redirect('society_mainpage', society_id=society.id) 
        else:
            messages.error(request, "Error in post creation. Please check the form.")
        
    else:
        form = PostForm()

    return render(request, 'society/create_post.html', {"form": form, "society": society})

def customise_society_view(request, society_id):
    society = get_object_or_404(Society, pk=society_id)
    
    past_colors = SocietyColorHistory.objects.filter(society=society).order_by('-updated_at')
    if request.method == 'POST':
        form = CustomisationForm(request.POST, instance=society)
        if form.is_valid():
            SocietyColorHistory.objects.create(
                society=society,
                previous_colour1=society.colour1,
                previous_colour2=society.colour2
            )

            form.save()
            return redirect('society_mainpage', society_id=society.id)
    else:
        form = CustomisationForm(instance=society)

    return render(request, 'society/customise_society.html', {
        'form': form,
        'society': society,
        'past_colors': past_colors 
    })

# Competition-related views

@login_required
def create_competition(request, society_id):
    if not request.user.is_committee_member():
        return HttpResponseForbidden("You are not a committee member in this society.")

    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.society_id = society_id
            competition.save()
            return redirect("manage_competitions", society_id=society_id)
    else:
        form = CompetitionForm()

    return render(request, "competitions/create_competition.html", {"form": form, "society_id": society_id})

     
# once match is scheduled, participants cant withdraw
# students should have the same option (without matchmaking power)-just withdraw
def manage_competitions(request, society_id):
    if not request.user.is_committee_member():
        return HttpResponseForbidden("You are not a committee member in this society.")

    competitions = Competition.objects.filter(society_id=society_id)
    return render(request, "competitions/manage_competitions.html", {
        "society_id": society_id,
        "competitions": competitions,
    })


@login_required
def create_team(request, competition_id):
    """Allow society admin to create a team and assign members to it."""
    competition = get_object_or_404(Competition, pk=competition_id, is_active=True, is_team_based=True)

    if not request.user.is_committee_member():
        return HttpResponseForbidden("You are not a committee member in this society.")

    if request.method == "POST":
        form = TeamCreationForm(competition=competition, data=request.POST)
        if form.is_valid():
            # Create the team
            team_name = form.cleaned_data["team_name"]
            new_team = Team.objects.create(competition=competition, name=team_name)

            # create a TeamMembership for each selected participant 
            selected_participants = form.cleaned_data["participants"] 
            for part_id in selected_participants:
                participant = CompetitionParticipant.objects.get(pk=part_id, competition=competition)
                TeamMembership.objects.create(user=participant.user, team=new_team)

            return redirect("competition_detail", competition_id=competition_id)
    else:
        form = TeamCreationForm(competition=competition)

    return render(request, "competitions/create_team.html", {
        "competition": competition,
        "form": form
    })


@login_required
def finalize_competition(request, competition_id):
    """Allows for finalizing lineup so no new joins/leaves."""
    competition = get_object_or_404(Competition, pk=competition_id)
    if not request.user.is_committee_member():
        return HttpResponseForbidden("You are not a committee member in this society.")

    # Finalize the competition lineup
    competition.is_finalized = True
    competition.save()
    return redirect("competition_detail", competition_id=competition_id)