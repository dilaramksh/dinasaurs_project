from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms.event_creation_form import EventCreationForm
from social_media.forms.post_creation import PostForm  
from social_media.forms.customise_society import customisationForm 
from social_media.models.colour_history import SocietyColorHistory
from social_media.models import Society, Event
from django.utils.timezone import now
from datetime import date


#@login_required
def society_dashboard(request):

    return render(request, 'society/society_dashboard.html')

def event_creation(request):
    
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            
            event.save()
            messages.success(request, "Your event has been created.")
            return redirect("society_dashboard") 
        else:                  
            messages.error(request, "There was an error with your submission. Please try again.")
    
    else:
        form = EventCreationForm()

    return render(request, 'society/event_creation.html', {'form': form})

def terminate_society(request):
    '''society = get_object_or_404(Society, founder=request.user)  

    if request.method == "POST":
        society.delete()
        return redirect("society_dashboard")  
    '''
    #return render(request, "terminate_society.html", {"society": society})
    return render(request, "society/terminate_society.html")

def view_members(request):

    return render(request, 'society/view_members.html')

def view_upcoming_events(request):

    events = Event.objects.filter(date__gte=date.today()).order_by("date")
    return render(request, 'society/view_upcoming_events.html', {'events': events})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user  
            post.save()
            messages.success(request, "Post created successfully!")  
            return redirect("society_dashboard") 
        else:
            messages.error(request, "Error in post creation. Please check the form.")
        
    else:
        form = PostForm()

    return render(request, 'society/create_post.html', {"form": form})

def customise_society_view(request, society_id):
    society = get_object_or_404(Society, pk=society_id)
    
    if request.method == 'POST':
        form = customisationForm(request.POST, instance=society)
        if form.is_valid():
            past_colours = SocietyColorHistory.objects.create(
                society=society,
                previous_colour1=society.colour1,
                previous_colour2=society.colour2
            )

            form.save()
            return redirect('society_mainpage', society_id=society.id)
    else:
        form = customisationForm(instance=society)

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
