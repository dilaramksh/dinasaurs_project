from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from unittest.mock import patch
from django.core.exceptions import ValidationError

from social_media.models import (
    University,
    Society,
    Membership,
    Competition,
    CompetitionParticipant,
    Match,
    Category,
    SocietyRole,
)

User = get_user_model()

class CompetitionViewsTests(TestCase):
    def setUp(self):
        """
        Set up shared objects:
          - University
          - Two Users (one committee, one normal)
          - Society, Category, SocietyRoles
          - Memberships
          - Competitions (ongoing and ended)
          - CompetitionParticipants and Matches
        """
        self.client = Client()

        # Create a University
        self.university = University.objects.create(name="King's College London")

        # Create two users
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass',
            first_name='John',
            last_name='Doe',
            email='john@kcl.ac.uk',
            user_type='student',
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
        )
        self.normal_user = User.objects.create_user(
            username='normaluser',
            password='normalpass',
            first_name='Jane',
            last_name='Doe',
            email='jane@kcl.ac.uk',
            user_type='student',
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
        )

        # Create a Category (for society)
        self.category = Category.objects.create(name='sports')

        # Create a Society
        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.admin_user,
            society_email='basketballclub@kcl.ac.uk',
            status='approved',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        # Create two SocietyRoles for committee (for simplicity, using same role for both)
        self.role_committee = SocietyRole.objects.create(
            society=self.society,
            role_name='President'
        )
        self.non_committee = SocietyRole.objects.create(
            society=self.society,
            role_name='Member'
        )

        # Create committee membership for admin_user and normal membership for normal_user
        self.membership_admin = Membership.objects.create(
            user=self.admin_user,
            society=self.society,
            society_role=self.role_committee,
        )
        self.membership_normal = Membership.objects.create(
            user=self.normal_user,
            society=self.society,
            society_role=self.non_committee,
        )

        # Create an ongoing competition (not finalized)
        self.competition = Competition.objects.create(
            name="1v1 Showdown",
            society=self.society,
            is_point_based=False,
            is_ongoing=True,
            is_finalized=False,
        )

        # Create participants for the competition
        self.participant_admin = CompetitionParticipant.objects.create(
            user=self.admin_user,
            competition=self.competition,
            is_eliminated=False,
            points=0
        )
        self.participant_normal = CompetitionParticipant.objects.create(
            user=self.normal_user,
            competition=self.competition,
            is_eliminated=False,
            points=0
        )

        # Create a finished match for round 1 with winner set (for winner-based)
        self.match1 = Match.objects.create(
            competition=self.competition,
            round_number=1,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
            is_finished=True,
            winner_participant=self.participant_admin
        )

        # Create an ended competition (not ongoing)
        self.ended_competition = Competition.objects.create(
            name="Old Competition",
            society=self.society,
            is_point_based=False,
            is_ongoing=False,
            is_finalized=False,
        )
        self.ended_participant = CompetitionParticipant.objects.create(
            user=self.normal_user,
            competition=self.ended_competition,
            is_eliminated=False,
            points=0
        )

    # Helper method to login as committee (admin)
    def login_admin(self):
        self.client.login(username='adminuser', password='adminpass')

    # Helper method to login as normal user
    def login_normal(self):
        self.client.login(username='normaluser', password='normalpass')

    ## Tests for manage_competitions

    def test_manage_competitions_access_as_committee(self):
        self.login_admin()
        url = reverse("manage_competitions", kwargs={"society_id": self.society.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.competition.name)

    def test_manage_competitions_forbidden_for_non_committee(self):
        self.login_normal()
        url = reverse("manage_competitions", kwargs={"society_id": self.society.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    ## Tests for finalize_competition

    def test_finalize_competition_not_logged_in(self):
        url = reverse("finalize_competition", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url)
        # Should redirect to login page (302)
        self.assertNotEqual(response.status_code, 200)

    def test_finalize_competition_forbidden_for_non_committee(self):
        self.login_normal()
        url = reverse("finalize_competition", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_finalize_competition_success(self):
        self.login_admin()
        url = reverse("finalize_competition", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, follow=True)
        self.competition.refresh_from_db()
        self.assertTrue(self.competition.is_finalized)
        self.assertRedirects(response, reverse("competition_details", kwargs={"competition_id": self.competition.id}))

    def test_finalize_competition_ended(self):
        """
        If competition is not ongoing (ended), finalization should not occur,
        and an error message should be added.
        """
        self.login_admin()
        url = reverse("finalize_competition", kwargs={"competition_id": self.ended_competition.id})
        response = self.client.post(url, follow=True)
        self.ended_competition.refresh_from_db()
        # Assuming our view uses messages.error when competition is ended.
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("cannot modify an ended competition" in str(m) for m in messages_list))
        self.assertFalse(self.ended_competition.is_finalized)

    ## Tests for competition_details

    def test_competition_details_get_as_admin(self):
        self.login_admin()
        url = reverse("competition_details", kwargs={"competition_id": self.competition.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.competition.name)
        # Check that latest winner is computed (participant admin was winner in match1)
        self.assertContains(response, "Yes")

    def test_competition_details_toggle_elimination(self):
        self.login_admin()
        self.competition.is_ongoing = True
        self.competition.save()
        url = reverse("competition_details", kwargs={"competition_id": self.competition.id})
        self.assertFalse(self.participant_normal.is_eliminated)
        response = self.client.post(url, data={
            "action": "toggle_elimination",
            "participant_id": self.participant_normal.id
        }, follow=True)

        self.participant_normal.refresh_from_db()
        self.assertTrue(self.participant_normal.is_eliminated)


    def test_competition_details_end_competition(self):
        self.login_admin()
        url = reverse("competition_details", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={"action": "end_competition"}, follow=True)
        self.competition.refresh_from_db()
        self.assertFalse(self.competition.is_ongoing)

    ## Tests for set_up_round

    def test_set_up_round_access_denied_for_non_committee(self):
        self.login_normal()
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_set_up_round_access_denied_if_competition_not_finalized(self):
        self.login_admin()
        # Our competition is not finalized by default? In our setup, competition is not finalized.
        self.competition.is_finalized = False
        self.competition.save()
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_set_up_round_add_match_invalid_pair(self):
        """Test POST with invalid match pairing (identical participants) should not create match."""
        self.login_admin()
        self.competition.is_finalized = True
        self.competition.save()
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "add_match",
            "scheduled_time": "2025-01-01 10:00:00",
            "match_0_participant1": self.participant_admin.id,
            "match_0_participant2": self.participant_admin.id,  # same participant; should skip
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Match.objects.filter(competition=self.competition, round_number=2).exists())

    def test_set_up_round_add_match_success(self):
        """Test valid match pairing creates a match."""
        self.login_admin()
        self.competition.is_finalized = True
        self.competition.save()
        # Create a new participant to pair with
        new_user = User.objects.create_user(
            username='newuser', password='newpass', first_name='New', last_name='User', email='new@kcl.ac.uk', user_type='student', university=self.university,
            start_date='2023-09-23', end_date='2026-05-06'
        )
        new_participant = CompetitionParticipant.objects.create(user=new_user, competition=self.competition)
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "add_match",
            "scheduled_time": "2025-01-01 10:00:00",
            "match_0_participant1": self.participant_admin.id,
            "match_0_participant2": new_participant.id,
        })
        self.assertEqual(response.status_code, 302)
        # Round number should be 2 (since round 1 exists and is finished)
        match = Match.objects.filter(competition=self.competition, round_number=2).first()
        self.assertIsNotNone(match)
        self.assertEqual(match.scheduled_time.strftime("%Y-%m-%d %H:%M:%S"), "2025-01-01 10:00:00")

    ## Tests for record_match_results

    def test_record_match_results_redirect_if_no_matches(self):
        """If no matches exist, should redirect to competition_details."""
        self.login_admin()
        # Create a new competition with no matches
        comp_no_matches = Competition.objects.create(
            name="Empty Competition", society=self.society, is_point_based=False, is_ongoing=True, is_finalized=True
        )
        url = reverse("record_match_results", kwargs={"competition_id": comp_no_matches.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("competition_details", kwargs={"competition_id": comp_no_matches.id}))

    def test_record_match_results_update_points(self):
        """Test update_points action for point-based competition."""
        self.competition.is_point_based = True
        self.competition.is_finalized = True
        self.competition.save()
        # Create a new match for round 1 in point-based comp.
        m = Match.objects.create(
            competition=self.competition,
            round_number=1,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
            is_finished=False,
            score_p1=5,
            score_p2=5,
        )
        self.login_admin()
        url = reverse("record_match_results", kwargs={"competition_id": self.competition.id})
        # Update points
        response = self.client.post(url, data={
            "action": "update_points",
            f"score_p1_{m.id}": "10",
            f"score_p2_{m.id}": "15",
        })
        self.assertEqual(response.status_code, 302)
        m.refresh_from_db()
        self.participant_admin.refresh_from_db()
        self.participant_normal.refresh_from_db()
        self.assertTrue(m.is_finished)
        # Delta for participant_admin: 10-5 = 5; for participant_normal: 15-5 = 10
        self.assertEqual(self.participant_admin.points, 5)
        self.assertEqual(self.participant_normal.points, 10)

    def test_record_match_results_pick_winner(self):
        """Test pick_winner action for winner-based competition."""
        self.competition.is_point_based = False
        self.competition.is_finalized = True
        self.competition.save()
        m = Match.objects.create(
            competition=self.competition,
            round_number=2,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
            is_finished=False
        )
        self.login_admin()
        url = reverse("record_match_results", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "pick_winner",
            f"winner_{m.id}": str(self.participant_normal.id),
        })
        m.refresh_from_db()
        self.assertTrue(m.is_finished)
        self.assertEqual(m.winner_participant, self.participant_normal)
        self.assertEqual(response.status_code, 302)

    def test_record_match_results_eliminate(self):
        """Test eliminate action in record_match_results view."""
        self.competition.is_finalized = True
        self.competition.save()
        # Create a match for round 1 so that record_match_results view is accessible
        Match.objects.create(competition=self.competition, round_number=1)
        self.login_admin()
        url = reverse("record_match_results", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "eliminate",
            "eliminate_participant_id": self.participant_normal.id
        })
        self.participant_normal.refresh_from_db()
        self.assertTrue(self.participant_normal.is_eliminated)
        self.assertEqual(response.status_code, 302)


    def test_set_up_round_skip_same_participants(self):
        """Skipping creation if participant1 == participant2"""
        self.login_admin()
        self.competition.is_finalized = True
        self.competition.save()
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "add_match",
            "match_0_participant1": self.participant_admin.id,
            "match_0_participant2": self.participant_admin.id,
        }, follow=True)
        # No match should be created
        self.assertFalse(Match.objects.filter(round_number=2).exists())

    def test_set_up_round_validation_error(self):
        """Trigger the ValidationError in match.clean()"""
        self.login_admin()
        self.competition.is_finalized = True
        self.competition.save()
        
        with patch("social_media.models.Match.clean", side_effect=ValidationError("invalid")):
            url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
            response = self.client.post(url, data={
                "action": "add_match",
                "match_0_participant1": self.participant_admin.id,
                "match_0_participant2": self.participant_normal.id,
            }, follow=True)
            # Should still return a page without crashing
            self.assertEqual(response.status_code, 200)

    def test_set_up_round_revert_match(self):
        """Deleting an existing match"""
        self.login_admin()
        self.competition.is_finalized = True
        self.competition.save()
        match = Match.objects.create(
            competition=self.competition,
            round_number=2,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
        )
        url = reverse("set_up_round", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "revert_match",
            "match_id": match.id
        }, follow=True)
        self.assertFalse(Match.objects.filter(pk=match.id).exists())

    def test_record_match_results_pick_winner_participant1(self):
        self.competition.is_point_based = False
        self.competition.is_finalized = True
        self.competition.save()
        m = Match.objects.create(
            competition=self.competition,
            round_number=2,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
            is_finished=False
        )
        self.login_admin()
        url = reverse("record_match_results", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "pick_winner",
            f"winner_{m.id}": str(self.participant_admin.id),
        })
        m.refresh_from_db()
        self.assertEqual(m.winner_participant, self.participant_admin)
        self.assertTrue(m.is_finished)

    def test_record_match_results_pick_winner_participant1(self):
        self.competition.is_point_based = False
        self.competition.is_finalized = True
        self.competition.save()
        m = Match.objects.create(
            competition=self.competition,
            round_number=2,
            participant1=self.participant_admin,
            participant2=self.participant_normal,
            is_finished=False
        )
        self.login_admin()
        url = reverse("record_match_results", kwargs={"competition_id": self.competition.id})
        response = self.client.post(url, data={
            "action": "pick_winner",
            f"winner_{m.id}": str(self.participant_admin.id),
        })
        m.refresh_from_db()
        self.assertEqual(m.winner_participant, self.participant_admin)
        self.assertTrue(m.is_finished)
