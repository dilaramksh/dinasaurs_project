from django.conf import settings
from django.contrib.auth import login
from social_media.mixins import LoginProhibitedMixin
from django.urls import reverse, NoReverseMatch
from django.views.generic.edit import FormView
from social_media.forms import SignUpForm
import os
from django.core.files.storage import default_storage
from social_media.models import User

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

class SignUpView(LoginProhibitedMixin, FormView):
    """
    Display the sign up screen and handle sign ups.

    This view handles the display of the sign up screen and the processing of user sign ups.
    It ensures that users who are already logged in cannot access the sign up page.

    Attributes:
        form_class (Form): The form class to be used for sign up.
        template_name (str): The template to be used for rendering the view.
        redirect_when_logged_in_url (str): URL to redirect to if the user is already logged in.
    """

    form_class = SignUpForm
    template_name = "general/sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        """
        Handle valid sign up form submission.

        This method handles the case where the sign up form is valid. It saves the user,
        handles the profile picture upload, logs in the user, and redirects to the success URL.

        Args:
            form (Form): The form containing the sign up information.

        Returns:
            HttpResponse: The response after a successful form submission.
        """
        print(f"Users before: {User.objects.count()}")
        user = form.save()
        print(f"Users after form.save(): {User.objects.count()}")

        uploaded_file = self.request.FILES.get("profile_picture")

        if uploaded_file:
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = f"profile_pictures/{user.username}{file_extension}"

            saved_path = default_storage.save(new_filename, uploaded_file)
            user.profile_picture.name = saved_path

        else:
            user.profile_picture = DEFAULT_PROFILE_PICTURE

        user.save()
        print(f"Users after user.save(): {User.objects.count()}")

        login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid sign up form submission.

        This method handles the case where the sign up form is invalid. It prints the form errors
        and renders the sign up template with the form errors.

        Args:
            form (Form): The form containing the invalid sign up information.

        Returns:
            HttpResponse: The response after an unsuccessful form submission.
        """
        print(f"Form errors: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Return the redirect URL after a successful sign up.

        This method returns the URL to redirect to after a successful sign up.

        Returns:
            str: The URL to redirect to.
        """
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)