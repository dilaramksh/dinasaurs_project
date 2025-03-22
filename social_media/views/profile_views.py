from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from social_media.models import User
from social_media.forms import UserForm, PasswordForm
from django.contrib.auth import login, logout
import boto3
import os

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Display user profile editing screen, and handle profile modifications.

    This view allows users to update their profile information, including their profile picture.
    It handles the removal of the old profile picture (if necessary) and uploads the new one to S3.

    Attributes:
        model (Model): The model to be updated.
        template_name (str): The template to be used for rendering the view.
        form_class (Form): The form class to be used for updating the profile.
    """

    model = User
    template_name = "general/profile.html"
    form_class = UserForm

    def get_object(self):
        """
        Return the user to be updated.

        This method retrieves the current user to be updated.

        Returns:
            User: The current user.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Handle valid profile update, remove old picture (if necessary), and upload new one.

        This method handles the profile update process, including the removal of the old profile picture
        and the upload of the new one to S3.

        Args:
            form (Form): The form containing the updated profile information.

        Returns:
            HttpResponse: The response after a successful form submission.
        """
        user = self.request.user
        new_picture = self.request.FILES.get('profile_picture')


        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        if new_picture and user.profile_picture != DEFAULT_PROFILE_PICTURE:
            try:
                s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=user.profile_picture.name)
            except Exception as e:
                messages.warning(self.request, f"Could not delete old profile picture: {e}")


        if new_picture:
            file_extension = os.path.splitext(new_picture.name)[1]
            s3.upload_fileobj(
                new_picture,
                settings.AWS_STORAGE_BUCKET_NAME,
                f"profile_pictures/{user.username}{file_extension}",
                ExtraArgs={"ACL": "public-read", "ContentType": new_picture.content_type}
            )
            user.profile_picture = f"profile_pictures/{user.username}{file_extension}"

        if not user.profile_picture:
            user.profile_picture = 'profile_pictures/default.jpg'

        user.save()

        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid profile update.

        This method handles the case where the profile update form is invalid.

        Args:
            form (Form): The form containing the invalid profile information.

        Returns:
            HttpResponse: The response after an unsuccessful form submission.
        """
        messages.error(self.request, "Profile could not be updated.")
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Return the redirect URL after a successful update.

        This method returns the URL to redirect to after a successful profile update.

        Returns:
            str: The URL to redirect to.
        """
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

class PasswordView(LoginRequiredMixin, FormView):
    """
    Display password change screen and handle password change requests.

    This view allows users to change their password.

    Attributes:
        template_name (str): The template to be used for rendering the view.
        form_class (Form): The form class to be used for changing the password.
    """

    template_name = 'general/password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """
        Pass the current user to the password change form.

        This method passes the current user to the password change form.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The keyword arguments for the form.
        """
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        Handle valid form by saving the new password.

        This method handles the case where the password change form is valid and saves the new password.

        Args:
            form (Form): The form containing the new password.

        Returns:
            HttpResponse: The response after a successful form submission.
        """
        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect the user after successful password change.

        This method returns the URL to redirect to after a successful password change.

        Returns:
            str: The URL to redirect to.
        """
        messages.add_message(self.request, messages.SUCCESS, "Password updated")
        return reverse('dashboard')
    
def log_out(request):
    """
    Log out the current user.

    This view logs out the current user and redirects to the homepage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A redirect to the homepage.
    """
    logout(request)
    return redirect('homepage')