from django.test import TestCase
from social_media.models import Competition, Society, User, University, Category
from django.utils.timezone import now, timedelta
from django.utils import timezone

class CompetitionModelTestCase(TestCase):
    def setUp(self):
        self.society = Society.objects.create(
            name="Test Society",
            founder=User.objects.create_user(
                username='@founder', email='founder@test.com', password='12345',
                first_name='Test', last_name='Founder', user_type='student',
                university=University.objects.create(name='Test Uni', domain='testuni.ac.uk'),
                start_date=now().date(), end_date=(now() + timedelta(days=365)).date()
            ),
            society_email='test@soc.com',
            description='Desc',
            category=Category.objects.create(name='Test'),
            paid_membership=False,
            price=0.0,
            colour1='#FFFFFF',
            colour2='#000000',
            termination_reason='operational',
            status='approved',
        )
        self.competition = Competition.objects.create(
            name="Spring Coding Challenge",
            society=self.society,  # assuming you've created a valid Society instance
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7),
            is_ongoing=True,
            is_point_based=True,
            is_finalized=False
        )

    def test_competition_creation(self):
        self.assertEqual(self.competition.name, "Spring Coding Challenge")

