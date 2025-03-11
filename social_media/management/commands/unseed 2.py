from django.core.management.base import BaseCommand, CommandError
from social_media.models import *


class Command(BaseCommand):
    """Build automation command to unseed the database."""

    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""
        try:
            University.objects.all().delete()
            User.objects.all().delete()
            Category.objects.all().delete()
            Event.objects.all().delete()
            EventsParticipant.objects.all().delete()
            Membership.objects.all().delete()
            News.objects.all().delete()
            #Post.objects.all().delete()
            Society.objects.all().delete()
            SocietyRole.objects.all().delete()


            print("Unseed successfully. All relevant data has been removed.")
        except Exception as e:
            print(f"An error occurred while unseeding: {e}")