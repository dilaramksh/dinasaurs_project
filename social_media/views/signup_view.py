from django.conf import settings
from django.contrib.auth import login
from social_media.mixins import LoginProhibitedMixin
from django.urls import reverse, NoReverseMatch
from django.views.generic.edit import FormView
from social_media.forms import SignUpForm

DEFAULT_PROFILE_PICTURE_URL = "profile_pictures/default.jpg"

class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "general/sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        user = form.save()
        if self.request.FILES.get("profile_picture"):
            user.profile_picture = self.request.FILES["profile_picture"]
        else: 
            user.profile_picture = DEFAULT_PROFILE_PICTURE_URL
        user.save()
        login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"Form errors: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
