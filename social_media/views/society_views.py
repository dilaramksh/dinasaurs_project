from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from social_media.forms.event_creation_form import EventCreationForm
from social_media.forms.post_creation import PostForm  
from social_media.models import Society


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

def terminate_society(request, society_id):
    society = get_object_or_404(Society, id=society_id)

    if request.method == "POST":
        society.delete()
        return redirect("society/society_dashboard")  

    return render(request, "terminate_society.html", {"society": society})

def view_members(request):

    return render(request, 'society/view_members.html')

def view_upcoming_events(request):

    return render(request, 'society/view_upcoming_events.html')

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post created successfully!")  
            return redirect("society/society_dashboard") 
        else:
            messages.error(request, "Error in post creation. Please check the form.")
    else:
        form = PostForm()  

    return render(request, 'society/create_post.html', {"form": form})


def society_mainpage(request):
    return render(request, 'society/society_mainpage.html')