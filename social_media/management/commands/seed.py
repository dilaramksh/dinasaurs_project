from django.core.management.base import BaseCommand
from social_media.models import *

user_fixtures = [
    {'first_name':'john', 'last_name':'doe', 'username':'@johndoe', 'email':'johndoe@kcl.ac.uk', 'user_type':'student', 'university':'kcl', 'start_date':'2023-09-23', 'end_date':'2026-05-06'},
    {'first_name':'jane', 'last_name':'doe', 'username':'@janedoe', 'email':'janedoe@kcl.ac.uk', 'user_type':'student', 'university':'kcl', 'start_date':'2022-09-24', 'end_date':'2025-05-07'},
    {'first_name':'paul', 'last_name':'poe', 'username':'@paulpoe', 'email':'paulpoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':'kcl', 'start_date': '1864-01-01', 'end_date':'2025-01-01'},
    {'first_name':'pauline', 'last_name':'poe', 'username':'@paulinepoe', 'email':'paulinepoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':'kcl', 'start_date': '1864-01-01', 'end_date':'2025-01-01'},
    {'first_name':'grace', 'last_name':'kelly', 'username':'@gracekelly', 'email':'gracekelly@ox.ac.uk', 'user_type':'super_admin', 'university':'ox', 'start_date': '1987-07-02', 'end_date':'2025-09-01'},
]

society_fixtures = [
    {'name':'society', 'founder':'jane doe', 'society_email':'society@kcl.ac.uk', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'category':'other', 'paid_membership':'false', 'price':'0.0', 'colour1':'#FFFFFF', 'colour2':'#FFF', 'status':'approved'}
]



class Command(BaseCommand):
    #USER_COUNT =
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        #self.students = []

    def handle(self, *args, **options):
        self.clear_data()
        self.create_users()
        #self.create_societies()

    def clear_data(self):
        """Clear existing data."""
        self.stdout.write('\nClearing existing data...')

        #User.objects.all().delete()
        #Society.objects.all().delete()

        self.stdout.write('\nExisting data cleared.')


    def create_users(self):
        self.generate_user_fixtures()

    def create_societies(self):
        self.generate_society_fixtures()


    def generate_user_fixtures(self):
        for data in user_fixtures:
            print(f"Creating User: {data['username']}, Type: {data['user_type']}")
            self.try_create_user(data)
        print("Users created successfully")


    def generate_society_fixtures(self):
        for data in society_fixtures:
            print(f"Creating Society: {data['name']}, Status: {data['status']}")
            self.try_create_society(data)
        print("Societies created successfully")


    def try_create_user(self, data):
        try:
            self.create_user(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating user {data['username']}: {str(e)}\n"))


    def try_create_society(self, data):
        try:
            self.create_society(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating society {data['name']}: {str(e)}\n"))


    def create_user(self, data):
        university_name = data['university']
        university, created = University.objects.get_or_create(name=university_name)

        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            user_type=data['user_type'],
            university=university,
            password=Command.DEFAULT_PASSWORD,
        )
        user.save()

    def create_society(self, data):

        founder_name = data['founder']
        founder, created = User.objects.get_or_create(username=founder_name)

        category_name = data['category']
        category, created = Category.objects.get_or_create(name=category_name)

        society = Society.objects.create_society(
            name=data['name'],
            founder=founder,
            society_email=data['society_email'],
            description=data['description'],
            category=category,
            paid_membership=data['paid_membership'],
            price=data['price'],
            colour1=data['colour1'],
            colour2=data['colour2'],
            status=data['status'],
        )
        society.save()









