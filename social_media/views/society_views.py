from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import User
from django.contrib import messages
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.forms.event_creation_form import EventCreationForm
from django.shortcuts import HttpResponse
from social_media.models import Category
from social_media.forms.post_creation import PostForm  
from social_media.models.post import Post 
from social_media.models import Society

#@user_type_required('student')
#@login_required
def society_browser(request):
    return render(request, 'student/society_browser.html')

def society_creation_request(request):
    # if request.user.user_type != "student":
    #     messages.error(request, "Only students can request a new society.")
    #     return redirect("society_homepage")
    if request.method == 'POST':
        form = SocietyCreationForm(request.POST)
        if form.is_valid():
            society = form.save(commit=False)
            # Save with status 'Pending'
            society.status = "pending" 
            society.founder = request.user
            society.save()
            messages.success(request, "Your society request has been submitted for approval.")
            return redirect("student_dashboard") 
        else:                  
            messages.error(request, "There was an error with your request submission. Please try again.")
    
    else:
        form = SocietyCreationForm()

    return render(request, 'student/submit_society_request.html', {'form': form})


def create_temp_category(request):
    """View to create a temporary category for testing."""
    temp_category, created = Category.objects.get_or_create(name="Temporary Category")
    
    if created:
        return HttpResponse(f"Created category: {temp_category.name}")
    else:
        return HttpResponse("Category already exists.")

def view_societies(request):
    return render(request, 'student/view_societies.html')

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