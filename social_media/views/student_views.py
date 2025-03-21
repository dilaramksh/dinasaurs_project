from social_media.decorators import user_type_required
from social_media.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import Category
from django.shortcuts import get_object_or_404
import os
from django.core.files.storage import default_storage


DEFAULT_SOCIETY_LOGO = "society_logos/default.jpg"

#@login_required
def help_page(request):
    return render(request, "partials/footer/help.html")


#@login_required
def society_browser(request):
    return render(request, 'student/society_browser.html')


def society_creation_request(request):
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
    student = request.user
    print(student.university)
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



def student_societies(request):
    student = request.user
    memberships = Membership.objects.filter(user=student)
    user_societies = [membership.society_role.society for membership in memberships]
    selected_society = None

    if request.method == 'GET' and 'society_id' in request.GET:
        society_id = request.GET['society_id']
        selected_society = get_object_or_404(Society, id=society_id)
        if selected_society not in user_societies:
            selected_society = None

    if selected_society:
        society_roles = SocietyRole.objects.filter(society=selected_society)
        committee_members = [
            membership for membership in Membership.objects.filter(society_role__society=selected_society)
            if membership.is_committee_member()
        ]

    else:
        society_roles = SocietyRole.objects.filter(society__in=user_societies)

        committee_members = [
            membership.user for membership in Membership.objects.filter(society_role__society__in=user_societies)
            if membership.is_committee_member()
        ]

    return render(request, 'student/student_societies.html', {
        'student': student,
        'user_societies': user_societies,
        'selected_society': selected_society,
        'society_roles': society_roles,
        'committee_members': committee_members,
    })

