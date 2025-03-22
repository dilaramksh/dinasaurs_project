from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from social_media.models import University
from django.contrib.auth.decorators import login_required


@login_required
def super_admin_dashboard(request):
    """
    Display the super admin dashboard.

    This view retrieves the number of pending university requests and renders the super admin dashboard.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered super admin dashboard page with the number of pending university requests.
    """
    number_pending = University.objects.filter(status="pending").count()

    return render(request, 'super_admin/super_admin_dashboard.html', {'number_pending': number_pending})

def university_requests(request):
    """
    Display the list of pending university requests.

    This view retrieves the list of universities with a pending status and renders the university requests page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered university requests page with the list of pending universities.
    """
    pending_universities = University.objects.filter(status="pending")
    return render(request, 'super_admin/university_requests.html', {'pending_universities': pending_universities})

def update_university_status(request, university_id, new_status):
    """
    Update the status of a university.

    This view handles the update of a university's status. It only allows updates through a POST request.
    If the request method is not POST, it returns a forbidden response.

    Args:
        request (HttpRequest): The request object.
        university_id (int): The ID of the university to be updated.
        new_status (str): The new status to be assigned to the university.

    Returns:
        HttpResponse: A redirect to the previous page or a forbidden response if the request method is not POST.
    """
    if request.method == "POST":
        university = get_object_or_404(University, id=university_id)
        university.status = new_status
        university.save()
        messages.success(request, f"{university.name} has been marked as {new_status}.")
        previous_page = request.META.get('HTTP_REFERER', 'university_requests')
        return redirect(previous_page)
    return HttpResponseForbidden("Invalid request method.")

def registered_universities(request):
    """
    Display the list of registered and blocked universities.

    This view retrieves the list of universities with an approved or blocked status and renders the registered universities page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered registered universities page with the list of registered and blocked universities.
    """
    context = {
        'registered': University.objects.filter(status="approved"),
        'blocked': University.objects.filter(status="blocked")
    }
    return render(request, 'super_admin/registered_universities.html', context)
