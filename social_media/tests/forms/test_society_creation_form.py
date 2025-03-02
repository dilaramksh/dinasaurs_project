from tkinter.font import names
from unicodedata import category

from django import forms
from django.test import TestCase
from social_media.forms import *
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import User, University, Society, Category


class SocietyCreationFormTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(
            name="King's College London 2",
            domain='@kcl2.ac.uk', #kcl2 because kcl fails unique constraint
        )

        user = User.objects.create(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
        )

        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        self.society = Society.objects.create(
            name= 'footballclub',
            founder=user,
            society_email='footballclub@kcl.ac.uk',
            description='football club',
            category=category,
            paid_membership=False,
        )

        self.form_input = {
            'name': 'footballclub',
            'society_email': 'footballclub@kcl.ac.uk',
            'description': 'football club',
            'category': self.society.category.id
        }

    def test_valid_form(self): # FAILING
        form = SocietyCreationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        print(form.errors)

    def test_form_has_necessary_fields(self):
        form = SocietyCreationForm(data=self.form_input)
        self.assertIn('name', form.fields)
        self.assertIn('society_email', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('category', form.fields)

    '''def test_form_uses_model_validation(self):
        self.form_input['name'] = 'invalid name' #these need to be added to form
        self.form_input['society'] = 'invalid email'
        self.form_input['description'] = 'invalid description'
        self.form_input['category'] = 'invalid category'
        form = SocietyCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())'''

    def test_form_must_save_correctly(self):
        society = Society.objects.get(name='footballclub')
        form = SocietyCreationForm(instance=society, data=self.form_input)
        before_count = Society.objects.count()
        form.save()
        after_count = Society.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(society.name, 'footballclub')
        self.assertEqual(society.society_email, 'footballclub@kcl.ac.uk')
        self.assertEqual(society.category.name, 'sports')
        self.assertEqual(society.status, 'pending')

