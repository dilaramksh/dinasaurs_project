from django.test import TestCase
from social_media.forms.society_role_form import SocietyRoleForm
from django.utils.timezone import now, timedelta
from social_media.models import User, University, Category, Society, SocietyRole
from social_media.forms.society_role_form import DeleteRoleForm

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
        self.category = Category.objects.create(name="Tech")
        self.society = Society.objects.create(
            name="Coding Society",
            founder=self.user,
            society_email="code@society.com",
            description="A society for coding lovers",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFFFFF",
            colour2="#000000",
            termination_reason="operational",
            status="approved"
        )

        SocietyRole.objects.create(society=self.society, role_name="President")
        SocietyRole.objects.create(society=self.society, role_name="Member")
        self.role_to_delete = SocietyRole.objects.create(society=self.society, role_name="Event Manager")


    def test_valid_role_name(self):
        """Test that SocietyRoleForm accepts a valid role name."""
        form_data = {'role_name': 'Treasurer'}
        form = SocietyRoleForm(data=form_data)
        self.assertTrue(form.is_valid())
    