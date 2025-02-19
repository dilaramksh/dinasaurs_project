from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from social_media.models import User
from social_media.forms import UserForm, PasswordForm
from django.contrib.auth import login, logout

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = User
    template_name = "general/profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the user to be updated."""
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please could not be updated")
        return super().form_invalid(form)

    def get_success_url(self):
        """Return the redirect URL after a successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

    """
    def get_success_url(self):
        Return redirect URL after successful update.
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    """

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
    """Log out the current user"""

    logout(request)
    return redirect('homepage')