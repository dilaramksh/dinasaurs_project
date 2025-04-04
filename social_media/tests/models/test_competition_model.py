from django.test import TestCase
from social_media.models import Competition, Society, User, University, Category, CompetitionParticipant, Match
from django.utils.timezone import now, timedelta
from django.utils import timezone

class CompetitionModelTestCase(TestCase):
    def setUp(self):
        self.university, _ = University.objects.get_or_create(
            name='Test Uni',
            domain='testuni.ac.uk'
        )
        self.society = Society.objects.create(
            name="Test Society",
            founder=User.objects.create_user(
                username='@founder', email='founder@test.com', password='12345',
                first_name='Test', last_name='Founder', user_type='student',
                university=self.university,
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

        self.user1 = User.objects.create_user(
            username='@user1', email='user1@test.com', password='12345',
            first_name='User', last_name='One', user_type='student',
            university=self.university,
            start_date=now().date(), end_date=(now() + timedelta(days=365)).date()
        )

        self.user2 = User.objects.create_user(
            username='@user2', email='user2@test.com', password='12345',
            first_name='User', last_name='Two', user_type='student',
            university=self.university,
            start_date=now().date(), end_date=(now() + timedelta(days=365)).date()
        )

        self.participant1 = CompetitionParticipant.objects.create(user=self.user1, competition=self.competition)
        self.participant2 = CompetitionParticipant.objects.create(user=self.user2, competition=self.competition)

    def test_competition_creation(self):
        self.assertEqual(self.competition.name, "Spring Coding Challenge")
        self.assertTrue(self.competition.is_point_based)
        self.assertFalse(self.competition.is_finalized)
        self.assertEqual(str(self.competition), "Test Society: Spring Coding Challenge")

    def test_competition_participant_str(self):
        self.assertEqual(str(self.participant1), "@user1 in Spring Coding Challenge")

    def test_match_str(self):
        match = Match.objects.create(
            competition=self.competition,
            participant1=self.participant1,
            participant2=self.participant2,
            round_number=1
        )
        self.assertIn("Match #", str(match))
        self.assertIn("Spring Coding Challenge", str(match))

    def test_get_opponents(self):
        match = Match.objects.create(
            competition=self.competition,
            participant1=self.participant1,
            participant2=self.participant2,
            round_number=1
        )
        self.assertEqual(match.get_opponents(), (self.participant1, self.participant2))

    def test_finalize_result(self):
        match = Match.objects.create(
            competition=self.competition,
            participant1=self.participant1,
            participant2=self.participant2,
            round_number=1
        )

        match.finalize_result(score1=3, score2=2, winner_part=self.participant1)
        self.assertTrue(match.is_finished)
        self.assertEqual(match.score_p1, 3)
        self.assertEqual(match.score_p2, 2)
        self.assertEqual(match.winner_participant, self.participant1)




