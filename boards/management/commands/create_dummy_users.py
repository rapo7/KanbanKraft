import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    help = 'Create 30 dummy users with realistic names and assign them to groups'

    def handle(self, *args, **kwargs):
        # Create Django Manager group
        django_manager_group, created = Group.objects.get_or_create(name='Manager')
        print(django_manager_group, created)

        # Create Faker instance
        fake = Faker()

        # Create 30 dummy users
        for i in range(1, 31):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@kanbankraft.com"
            password = make_password('123456')

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            # Assign users to groups
            if i <= 10:
                user.groups.add(django_manager_group)
            user.save()

        # Get all tasks
        from boards.models import Task
        tasks = Task.objects.all()

        # Assign 10 users to tasks randomly
        users = User.objects.all()
        for task in tasks:
            user = random.choice(users)
            task.assigned_to = user
            task.save()

            # Remove assigned user from available users list
            users = users.exclude(id=user.id)

        self.stdout.write(self.style.SUCCESS('Dummy users created and tasks assigned successfully!'))
