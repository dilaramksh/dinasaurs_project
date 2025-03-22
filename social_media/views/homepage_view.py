from django.utils import timezone
from django.db.models import Count
import random
from django.shortcuts import redirect, render, get_object_or_404
from social_media.helpers import login_prohibited
from django.contrib import messages
from social_media.forms.university_creation_form import UniversityCreationForm
from social_media.models import University, Membership, Event, Society

DEFAULT_UNIVERSITY_LOGO = "university_logos/default.png"

@login_prohibited
def homepage(request):
    """Render the homepage. """
    return render(request, 'homepage.html')

def discover_universities(request):
    """Render the discover universities page with a list of approved universities."""
    universities = University.objects.filter(status='approved')
    return render(request, 'homepage/discover_universities.html', {'universities': universities})

def why_join_society(request):
    """Render the why join society page with popular societies, their first members, and upcoming events."""
    popular_societies = Society.objects.annotate(member_count=Count("membership")).order_by("-member_count")[:4]

    def get_first_member(society):
        """ Get the first member of a society.  """
        if society:
            return Membership.objects.filter(society=society).order_by("id").first()
        return None

    art_society = Society.objects.filter(name__icontains="art").first()
    gaming_society = Society.objects.filter(name__icontains="gaming").first()
    swim_society = Society.objects.filter(name__icontains="swim").first()

    art_member = get_first_member(art_society)
    swim_member = get_first_member(swim_society)
    gaming_member = get_first_member(gaming_society)

    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by("date")[:3]

    context = {
        'popular_societies': popular_societies,
        'art_member': art_member,
        'gaming_member': gaming_member,
        'swim_member': swim_member,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'homepage/why_join_society.html', context)

def latest_news(request):
    """Render the latest news page. """
    return render(request, 'homepage/latest_news.html')

def register_your_university(request):
    """ Handle the university registration form submission. """
    if request.method == 'POST':
        form = UniversityCreationForm(request.POST, request.FILES)

        if form.is_valid():
            university = form.save(commit=False)

            if 'logo' in request.FILES:
                university.logo = request.FILES['logo']
            else:
                university.logo = DEFAULT_UNIVERSITY_LOGO

            university.save()
            messages.success(request, "Your University request has been submitted for approval.")
            return redirect("homepage")
        else:
            messages.error(request, "There was an error with your request submission. Please try again.")
    else:
        form = UniversityCreationForm()

    return render(request, 'homepage/register_your_university.html', {'form': form})