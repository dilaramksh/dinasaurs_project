from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership, SocietyRole

@login_required
def change_society_status(request, society_id):
    """Allows university admin to change a society's status to approved, blocked, or pending."""
    if request.user.user_type != "uni_admin":
        return HttpResponseForbidden("You must be a university admin to do this.")

    if request.method == "POST":
        society = get_object_or_404(Society, pk=society_id)
        next_status = request.POST.get("next_status")

        if next_status not in ["approved", "blocked", "pending"]:
            next_status = "pending"

        if next_status == "approved":
            society.status = "approved"
            society.save()

            president, _ = SocietyRole.objects.get_or_create(
                society=society,
                role_name="President"
            )
            
            existing_membership = Membership.objects.filter(
            user=society.founder, 
            society=society
            ).first()

            if existing_membership:
                if existing_membership.society_role != president:
                    existing_membership.society_role = president
                    existing_membership.save()
            else:
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
    """ Allows university admin to view details of a pending society request."""
    society = get_object_or_404(Society, pk=society_id)

    if request.user.user_type != "uni_admin":
        return HttpResponseForbidden("You must be a university admin to view this.")

    if society.founder.university != request.user.university:
        return HttpResponseForbidden("You can only review requests from your university.")

    context = {
        "society": society
    }

    return render(request, "uni_admin/society_request_details.html", context)