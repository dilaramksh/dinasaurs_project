# social_media/views/__init__.py

from .login_view import LogInView
from .signup_view import SignUpView
from .profile_views import ProfileUpdateView, PasswordView, log_out
from .homepage_view import homepage
from .dashboard_views import dashboard, get_society_dashboard
from .student_views import (
    society_browser, view_societies, society_creation_request
)
from .society_views import (
    event_creation, terminate_society, view_members, view_upcoming_events, create_post
)
from .membership_view import view_memberships