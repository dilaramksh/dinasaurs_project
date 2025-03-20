from django.core.management.base import BaseCommand
from social_media.models import University

"""Seeder for a list of predefined ("verified") universities."""
class Command(BaseCommand):
    help = "Seed the database with verified universities."

    UNIVESITIES = [
        {"name": "King's College London", "domain": "kcl.ac.uk"},
        {"name": "University College London", "domain": "ucl.ac.uk"},
        {"name": "Imperial College London", "domain": "imperial.ac.uk"},
        {"name": "London School of Economics", "domain": "lse.ac.uk"},
        {"name": "University of Oxford", "domain": "ox.ac.uk"},
    ]

    def handle(self, *args, **options):
        self.generate_all_univeristies()
    
    def generate_all_univeristies(self):
        for uni in self.UNIVESITIES:
            university, created = University.objects.get_or_create(
                name=uni['name'],
                defaults={'domain': uni['domain']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created university: {university.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"University already exists: {university.name}"))

        self.stdout.write(self.style.SUCCESS("University seeding complete."))
