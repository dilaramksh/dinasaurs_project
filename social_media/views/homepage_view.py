from django.shortcuts import redirect, render
from social_media.helpers import login_prohibited
from django.contrib import messages
from social_media.forms.university_creation_form import UniversityCreationForm

@login_prohibited
def homepage(request):
    return render(request, 'homepage.html')

def discover_universities(request):
    return render(request, 'homepage/discover_universities.html')

def why_join_society(request):
    return render(request, 'homepage/why_join_society.html')


def latest_news(request):
    return render(request, 'homepage/latest_news.html')

def register_your_university(request):
    if request.method == 'POST':
        form = UniversityCreationForm(request.POST)
        if form.is_valid():
            university = form.save(commit=False)
            university.status = "pending"
            university.save()
            messages.success(request, "Your society request has been submitted for approval.")
            return redirect("homepage") 
        else:                  
            messages.error(request, "There was an error with your request submission. Please try again.")
    else:
        form = UniversityCreationForm()

    return render(request, 'homepage/register_your_university.html', {'form': form})