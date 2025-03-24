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
    """Display user profile editing screen, and handle profile modifications."""

    model = User
    template_name = "general/profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the user to be updated."""
        return self.request.user

    def form_valid(self, form):
        """Handle valid profile update, remove old picture (if necessary), and upload new one."""
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
                ExtraArgs={"ContentType": new_picture.content_type}
            )
            user.profile_picture = f"profile_pictures/{user.username}{file_extension}"

        if(not user.profile_picture):
            user.profile_picture = DEFAULT_PROFILE_PICTURE

        user.save()
        user.refresh_from_db()

        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid profile update."""
        messages.error(self.request, "Profile could not be updated.")
        return super().form_invalid(form)

    def get_success_url(self):
        """Return the redirect URL after a successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""
    template_name = 'general/password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""
        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""
        messages.add_message(self.request, messages.SUCCESS, "Password updated")
        return reverse('dashboard')
    
def log_out(request):
    """Log out the current user. """
    logout(request)
    return redirect('homepage')