# Generated by Django 4.2.18 on 2025-03-22 21:23

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(help_text='Enter a username starting with "@" followed by at least three alphanumeric characters.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username must start with @ followed by at least three alphanumeric characters (letters, numbers, or underscore).', regex='^@\\w{3,}$')])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('user_type', models.CharField(choices=[('super_admin', 'Super Admin'), ('uni_admin', 'University Admin'), ('student', 'Student')], default='student', max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('cultural', 'Cultural'), ('academic_career', 'Academic and Career'), ('faith', 'Faith'), ('political', 'Political'), ('sports', 'Sports'), ('volunteering', 'Volunteering'), ('other', 'Other')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_ongoing', models.BooleanField(default=True)),
                ('is_point_based', models.BooleanField(default=False)),
                ('is_finalized', models.BooleanField(default=False, help_text='If True, no new participants can join or be modified.')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_eliminated', models.BooleanField(default=False)),
                ('points', models.FloatField(blank=True, default=0.0)),
                ('rank', models.PositiveIntegerField(blank=True, null=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='social_media.competition')),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=1000)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=250)),
                ('picture', models.ImageField(blank=True, default='events_picture/default.jpg', null=True, upload_to='events_picture/')),
            ],
        ),
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('society_email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('description', models.CharField(max_length=2000)),
                ('paid_membership', models.BooleanField(default=False)),
                ('price', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, message='Price cannot be negative.'), django.core.validators.MaxValueValidator(50.0)])),
                ('colour1', models.CharField(default='#FFD700', max_length=7, validators=[django.core.validators.RegexValidator(message='Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])),
                ('colour2', models.CharField(default='#FFF2CC', max_length=7, validators=[django.core.validators.RegexValidator(message='Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])),
                ('logo', models.ImageField(blank=True, default='society_logos/default.png', null=True, upload_to='society_logos/')),
                ('termination_reason', models.CharField(choices=[('operational', 'Operational reasons'), ('low_interest', 'Low Interest'), ('financial', 'Financial reasons'), ('other', 'Other reason')], max_length=50)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('blocked', 'Blocked')], default='pending', max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.category')),
                ('founder', models.ForeignKey(limit_choices_to={'user_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('domain', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message="Domain must contain at least three alphanumerics, and end with '.ac.uk'.", regex='\\w{3,}\\.ac\\.uk$')])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('blocked', 'Blocked')], default='pending', max_length=20)),
                ('logo', models.ImageField(blank=True, default='university_logos/default.png', null=True, upload_to='university_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='SocietyRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=50)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.society')),
            ],
        ),
        migrations.CreateModel(
            name='SocietyColorHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_colour1', models.CharField(max_length=7)),
                ('previous_colour2', models.CharField(max_length=7)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_history', to='social_media.society')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, default=None, null=True, upload_to='post_pictures/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='social_media.society')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.society')),
                ('society_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.societyrole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.PositiveIntegerField(default=1)),
                ('scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('score_p1', models.FloatField(blank=True, null=True)),
                ('score_p2', models.FloatField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='social_media.competition')),
                ('participant1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p1_matches', to='social_media.competitionparticipant')),
                ('participant2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p2_matches', to='social_media.competitionparticipant')),
                ('winner_participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_won', to='social_media.competitionparticipant')),
            ],
        ),
        migrations.CreateModel(
            name='EventsParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.event')),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.membership')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.society'),
        ),
        migrations.AddField(
            model_name='competition',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='social_media.society'),
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media.university'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='societyrole',
            constraint=models.UniqueConstraint(fields=('society', 'role_name'), name='unique_society_role'),
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('user', 'society'), name='unique_user_in_society'),
        ),
        migrations.AddConstraint(
            model_name='eventsparticipant',
            constraint=models.UniqueConstraint(fields=('event', 'membership'), name='unique_events_participant'),
        ),
        migrations.AlterUniqueTogether(
            name='competitionparticipant',
            unique_together={('user', 'competition')},
        ),
    ]
