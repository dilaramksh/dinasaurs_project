from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from social_media.models import University
from django.contrib.auth.decorators import login_required


@login_required
def super_admin_dashboard(request):
    """Display the super admin dashboard."""
    number_pending = University.objects.filter(status="pending").count()

    return render(request, 'super_admin/super_admin_dashboard.html', {'number_pending': number_pending})

def university_requests(request):
    """Display the list of pending university requests."""
    pending_universities = University.objects.filter(status="pending")
    return render(request, 'super_admin/university_requests.html', {'pending_universities': pending_universities})

def update_university_status(request, university_id, new_status):
    """Update the status of a university. """
    if request.method == "POST":
        university = get_object_or_404(University, id=university_id)
        university.status = new_status
        university.save()
        messages.success(request, f"{university.name} has been marked as {new_status}.")
        previous_page = request.META.get('HTTP_REFERER', 'university_requests')
        return redirect(previous_page)
    return HttpResponseForbidden("Invalid request method.")

def registered_universities(request):
    """ Display the list of registered and blocked universities. """
    context = {
        'registered': University.objects.filter(status="approved"),
        'blocked': University.objects.filter(status="blocked")
    }
    return render(request, 'super_admin/registered_universities.html', context)
