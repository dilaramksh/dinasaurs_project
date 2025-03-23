from django.test import TestCase
from django.utils.timezone import now, timedelta
from social_media.forms.society_role_form import SocietyRoleForm, DeleteRoleForm
from social_media.models import Society, User, University, Category, SocietyRole

class SocietyRoleFormTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(name="Test University", domain="testuni123.ac.uk")
        self.user = User.objects.create_user(
            username='@testuser',
            email='testuser@test.com',
            password='12345',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
        self.category = Category.objects.create(name="Tech")
        self.society = Society.objects.create(
            name="Tech Society",
            founder=self.user,
            society_email="tech@society.com",
            description="A society for tech enthusiasts.",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFFFFF",
            colour2="#000000",
            termination_reason="operational",
            status="approved"
        )
        # Create some roles
        self.president_role = SocietyRole.objects.create(society=self.society, role_name="President")
        self.member_role = SocietyRole.objects.create(society=self.society, role_name="Member")
        self.custom_role = SocietyRole.objects.create(society=self.society, role_name="Designer")

    def test_society_role_form_valid(self):
        form_data = {'role_name': 'Developer'}
        form = SocietyRoleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_delete_role_form_queryset_excludes_president_and_member(self):
        form = DeleteRoleForm(society=self.society)
        roles_in_form = list(form.fields['role'].queryset.values_list('role_name', flat=True))
        self.assertNotIn('President', roles_in_form)
        self.assertNotIn('Member', roles_in_form)
        self.assertIn('Designer', roles_in_form)

    def test_delete_role_form_no_society(self):
        form = DeleteRoleForm()
        self.assertEqual(list(form.fields['role'].queryset), [])
