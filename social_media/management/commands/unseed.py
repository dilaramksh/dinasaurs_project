from django.core.management.base import BaseCommand, CommandError
from social_media.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        """Unseed the database."""
        try:
            User.objects.all().delete()
            Category.objects.all().delete()
            Event.objects.all().delete()
            EventsParticipant.objects.all().delete()
            Membership.objects.all().delete()
            News.objects.all().delete()
            #Post.objects.all().delete()
            Society.objects.all().delete()
            SocietyRole.objects.all().delete()
            University.objects.all().delete()
            print(f"Unseeded the database successfully.")

        except Exception as e:
            print(f"An error occurred while unseeding: {e}")

