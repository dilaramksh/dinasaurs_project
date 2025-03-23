from django.test import TestCase
from social_media.forms.society_role_form import SocietyRoleForm
from django.utils.timezone import now, timedelta
from social_media.models import User, University

class SocietyRoleFormTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(name="Test Uni", domain="testuni1.ac.uk")
        self.user = User.objects.create_user(
            username='@tester',
            email='tester@example.com',
            password='testpass',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
    def test_valid_role_name(self):
        """Test that SocietyRoleForm accepts a valid role name."""
        form_data = {'role_name': 'Treasurer'}
        form = SocietyRoleForm(data=form_data)
        self.assertTrue(form.is_valid())
    