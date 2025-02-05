from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.forms.event_creation_form import EventCreationForm
from django.shortcuts import HttpResponse
from social_media.models import Category

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

    return render(request, 'society/terminate_society.html')

def view_members(request):

    return render(request, 'society/view_members.html')

def create_post(request):

    return render(request, 'society/create_post.html')

def view_upcoming_events(request):

    return render(request, 'society/view_upcoming_events.html')
