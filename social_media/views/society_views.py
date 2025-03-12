from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms import CustomisationForm, PostForm, EventCreationForm, DeleteRoleForm, SocietyRoleForm
from social_media.models.colour_history import SocietyColorHistory
from social_media.models import Society, Event, Membership, EventsParticipant, SocietyRole
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
        "society_id" : society_id
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
        form = PostForm(request.POST, request.FILES)
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

def manage_committee(request, society_id):
    memberships = Membership.objects.filter(society_id=society_id).select_related('user', 'society_role')
    committee_members = [m.user for m in memberships if m.society_role.is_committee_role()]
    
    all_users = list(set(m.user for m in memberships))

    context = {
        "committee_members": committee_members,
        "users": all_users,  
        "society_id" : society_id
    }
    return render(request, 'society/manage_committee.html', context)

def edit_roles(request, society_id):
    society = get_object_or_404(Society, id=society_id)
    roles = SocietyRole.objects.filter(society=society) 

    committee_roles = [role for role in roles if role.is_committee_role()]

    if request.method == "POST":
        if 'add_role' in request.POST:
            add_form = SocietyRoleForm(request.POST)
            if add_form.is_valid():
                new_role = add_form.save(commit=False)
                new_role.society = society
                new_role.save()
                return redirect('edit_roles', society_id=society.id)

        elif 'delete_role' in request.POST:
            delete_form = DeleteRoleForm(request.POST, society=society)
            if delete_form.is_valid():
                role_to_delete = delete_form.cleaned_data['role']
                role_to_delete.delete()
                return redirect('edit_roles', society_id=society.id)
    else:
        add_form = SocietyRoleForm()
        delete_form = DeleteRoleForm(society=society)

    return render(request, 'society/edit_roles.html', {
        'society': society,
        'committee_roles': committee_roles,
        'add_form': add_form,
        'delete_form': delete_form
    })