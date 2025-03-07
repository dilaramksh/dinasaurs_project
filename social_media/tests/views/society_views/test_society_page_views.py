from unicodedata import category

from django.test import TestCase
from django.urls import reverse

from social_media.models import *


class SocietyPageViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        user = User.objects.create(
            first_name='john',
            last_name='doe',
            email='johndoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johndoe',
        )

        self.society = Society.objects.create(
            name='basketballclub',
            founder=user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=category,
            paid_membership=False,
        )

    def test_society_mainpage_view(self):
        response = self.client.get(reverse('society_mainpage', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'society/society_mainpage.html')
