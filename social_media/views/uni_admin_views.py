from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from social_media.models import Society, Membership, SocietyRole

@login_required
def change_society_status(request, society_id):
    """Allows uni admin to change a society's status to approved, blocked, or pending."""
    if request.user.user_type != "uni_admin":
        return HttpResponseForbidden("You must be a university admin to do this.")


    if request.method == "POST":
        society = get_object_or_404(Society, pk=society_id)
        next_status = request.POST.get("next_status")

        if next_status not in ["approved", "blocked", "pending"]:
            # fallback
            next_status = "pending"

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
            society.save()
            return redirect("dashboard")  

        else:
            society.status = "pending"
            society.save()

        return redirect("dashboard")


    return HttpResponseNotAllowed(["POST"])
