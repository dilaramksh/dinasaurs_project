from django.test import TestCase
from social_media.forms.society_role_form import SocietyRoleForm

class SocietyRoleFormTests(TestCase):
    def test_valid_role_name(self):
        """Test that SocietyRoleForm accepts a valid role name."""
        form_data = {'role_name': 'Treasurer'}
        form = SocietyRoleForm(data=form_data)
        self.assertTrue(form.is_valid())
    