from social_media.decorators import user_type_required
from social_media.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import Category, Competition, CompetitionParticipant
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
import os
from django.core.files.storage import default_storage


DEFAULT_SOCIETY_LOGO = "society_logos/default.png"

#@login_required
def help_page(request):
    """Render the help page. """
    return render(request, "partials/footer/help.html")


#@login_required

def society_creation_request(request):
    """Handle the society creation request form submission."""
    if request.method == 'POST':
        form = SocietyCreationForm(request.POST)
        if form.is_valid():
            society = form.save(commit=False)
            society.status = "pending" 
            society.founder = request.user

            uploaded_file = request.FILES.get("logo")

            if uploaded_file:
                file_extension = os.path.splitext(uploaded_file.name)[1]
                new_filename = f"society_logos/{society.name}{file_extension}"

                saved_path = default_storage.save(new_filename, uploaded_file)
                society.logo = saved_path

            else:
                society.logo = DEFAULT_SOCIETY_LOGO

            society.save()
            messages.success(request, "Your society request has been submitted for approval.")
            return redirect("dashboard") 
        else:                  
            messages.error(request, "There was an error with your request submission. Please try again.")
    
    else:
        form = SocietyCreationForm()

    return render(request, 'student/submit_society_request.html', {'form': form})


def view_societies(request):
    """ Display the list of approved societies for the current user's university."""
    student = request.user
    societies = Society.objects.filter(founder__university=student.university, status="approved").prefetch_related('posts')    
    categories = Category.objects.all()

    # Get search query
    search_query = request.GET.get('search', '')
    if search_query:
        societies = societies.filter(name__icontains=search_query)

    # Get category filter
    category_id = request.GET.get('category', '')
    if category_id:
        societies = societies.filter(category_id=category_id)

    society_posts = {society.id: society.posts.all() for society in societies}

    return render(request, 'student/view_societies.html', {
        'societies': societies,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'society_posts': society_posts
    })


@login_required
def view_competitions(request):
    """Shows all competitions by societies user is a member of"""
    student = request.user
    print(student.university)
    societies = Society.objects.filter(founder__university=student.university, status="approved").prefetch_related('competitions')    
    categories = Category.objects.all()

  
    society_competitions = Competition.objects.filter(society__in=societies)

    return render(request, 'student/view_competitions.html', {
        'societies': societies,
        'categories': categories,
        'society_competitions': society_competitions
    })


@login_required
def view_my_competitions(request):
    """Shows all competitions current user takes part in"""
    user = request.user
    
    if user.user_type != 'student':
        return HttpResponseForbidden("This page is for students only.")

    user_participations = CompetitionParticipant.objects.filter(user=user)

    competitions = []
    for part in user_participations:
        comp = part.competition
        comp_info = {
            "id": comp.id,
            "name": comp.name,
            "is_ongoing": comp.is_ongoing,
            "is_point_based": comp.is_point_based,
            "is_finalized": comp.is_finalized,
            "eliminated": part.is_eliminated,
        }
        competitions.append(comp_info)

    
    return render(request, "student/view_my_competitions.html", {
        "competitions": competitions,
    })


@login_required
def join_competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    

    # joining not allowed if finalized
    if competition.is_finalized:
        return HttpResponseForbidden("You can no longer join this competition; it's finalized.")

    # ensure user not already joined
    if CompetitionParticipant.objects.filter(user=request.user, competition=competition).exists():
        messages.error(request, "You have already joined this competition.")
        return redirect("competition_details", competition_id=competition_id) 

    CompetitionParticipant.objects.create(user=request.user, competition=competition)
    messages.success(request, "You successfully signed up for this competition")
    return redirect("competition_details", competition_id=competition_id) 


@login_required
def leave_competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    # leaving not allowed if finalized
    if competition.is_finalized:
        return HttpResponseForbidden("Competition is finalized. You can't leave now.")

    participant = get_object_or_404(CompetitionParticipant, user=request.user, competition=competition)
    participant.delete()
    return redirect("view_my_competitions")

