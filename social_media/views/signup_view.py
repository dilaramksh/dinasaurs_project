from django.conf import settings
from django.contrib.auth import login
from social_media.mixins import LoginProhibitedMixin
from django.urls import reverse
from django.views.generic.edit import FormView
from social_media.forms import SignUpForm
import os
from django.core.files.storage import default_storage

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""
    form_class = SignUpForm
    template_name = "general/sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        user = form.save()

        uploaded_file = self.request.FILES.get("profile_picture")

        if uploaded_file:
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = f"profile_pictures/{user.username}{file_extension}"

            saved_path = default_storage.save(new_filename, uploaded_file)
            user.profile_picture.name = saved_path

        else:
            user.profile_picture = DEFAULT_PROFILE_PICTURE

        user.save()

        login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid sign up form submission."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """Return the redirect URL after a successful sign up."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)