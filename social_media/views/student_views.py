from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from social_media.forms.society_creation_form import SocietyCreationForm
from django.shortcuts import HttpResponse
from social_media.models import Category

#to do: add login required
#to do: add user type required

@user_type_required('student')
@login_required
def student_dashboard(request):
    student = request.user

    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    print("User Societies:", user_societies)  # Debugging print

    events = Event.objects.filter(society__in=user_societies)
    print("Events:", events)  # Debugging print

    if not memberships:
        print("No memberships found for this user")
    if not user_societies:
        print("No societies found for this user")
    if not events:
        print("No events found for this user")

    return render(request, 'student/student_dashboard.html', {
        'student': student,
        'user_societies': user_societies,
        'user_events': events
    })

#Views for pages from dropdown menu in Student Navbar
#@login_required
def help(request):
    return render(request, 'help.html')

#@login_required
def features(request):
    return render(request, 'features.html')

#@login_required
def pricing(request):
    return render(request, 'pricing.html')

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
