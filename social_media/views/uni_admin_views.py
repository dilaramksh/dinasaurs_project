from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership, SocietyRole

@login_required
def change_society_status(request, society_id):
    """
    Allows university admin to change a society's status to approved, blocked, or pending.

    This view allows a university admin to change the status of a society. It handles the status
    change through a POST request and ensures that the user is a university admin. If the status
    is changed to approved, it assigns the founder as the President of the society.

    Args:
        request (HttpRequest): The request object.
        society_id (int): The ID of the society to be updated.

    Returns:
        HttpResponse: A redirect to the dashboard with the updated status or a forbidden/not allowed response.
    """
    if request.user.user_type != "uni_admin":
        return HttpResponseForbidden("You must be a university admin to do this.")

    if request.method == "POST":
        society = get_object_or_404(Society, pk=society_id)
        next_status = request.POST.get("next_status")

        if next_status not in ["approved", "blocked", "pending"]:
            next_status = "pending"  # fallback

        if next_status == "approved":
            society.status = "approved"
            society.save()

            # Create or get 'President' role for this society
            president, _ = SocietyRole.objects.get_or_create(
                society=society,
                role_name="President"
            )
            if not Membership.objects.filter(
                    user=society.founder,
                    society_role=president
                ).exists():
                Membership.objects.create(
                    user=society.founder,
                    society=society,
                    society_role=president
                )

        elif next_status == "blocked":
            society.status = "blocked"
            society.save()

        else:
            society.status = "pending"
            society.save()

        return redirect(f"/dashboard/?status={next_status}")

    return HttpResponseNotAllowed(["POST"])

@login_required
def society_request_details(request, society_id):
    """
    Allows university admin to view details of a pending society request.

    This view allows a university admin to view the details of a pending society request. It ensures
    that the user is a university admin and that the society belongs to the same university as the admin.

    Args:
        request (HttpRequest): The request object.
        society_id (int): The ID of the society to be viewed.

    Returns:
        HttpResponse: The rendered society request details page or a forbidden response.
    """
    society = get_object_or_404(Society, pk=society_id)

    if request.user.user_type != "uni_admin":
        return HttpResponseForbidden("You must be a university admin to view this.")

    if society.founder.university != request.user.university:
        return HttpResponseForbidden("You can only review requests from your university.")

    context = {
        "society": society
    }

    return render(request, "uni_admin/society_request_details.html", context)