from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms.event_creation_form import EventCreationForm
from social_media.forms.post_creation import PostForm  
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
    society = get_object_or_404(Society, founder=request.user)  

    if request.method == "POST":
        society.delete()
        return redirect("society_dashboard")  

    return render(request, "terminate_society.html", {"society": society})

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
