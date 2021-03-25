from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from users.models import UserProfile
from questions.models import *

from random import choice
from faker import Faker

f = Faker()

class Command(BaseCommand):
    help = 'Fill db with objects from users and questions apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            action='store',
            nargs='?',
            type=int,
            default=20,
            help='users count'
        )
        parser.add_argument(
            '-q',
            '--questions',
            action='store',
            nargs='?',
            type=int,
            default=100,
            help='questions count'
        )
        parser.add_argument(
            '-a',
            '--max_answers_per_question',
            action='store',
            nargs='?',
            type=int,
            default=25,
            help='max answers per question count'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store',
            nargs='?',
            type=int,
            default=20,
            help='tags count'
        )


    def handle(self, *args, **options):
        self.fill_users(options['users'])
        self.fill_tags(options['tags'])
        self.fill_questions_and_answers(options['questions'], options['max_answers_per_question'])

    def fill_users(self, count):
        for i in range(count):
            password = f.password()
            user = User(username=f.user_name(), email=f.email())
            user.set_password(password)
            user.save()
            UserProfile.objects.create(
                user_id=user.id,
                nick_name=user.username
            )
            if (i == 0):
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print('You can login in django-admin with this credentials:')
                print('username:', user.username)
                print('password:', password)

    def fill_tags(self, count):
        for i in range(count):
            Tag.objects.create(
                title=(f.word() + str(f.random_int(min=1, max=100)))
            )

    def fill_questions_and_answers(self, count, max_answers):
        author_ids = list(UserProfile.objects.values_list('id', flat=True))
        tags_ids = (Tag.objects.values_list('id', flat=True))
        for i in range(count):
            r_id = Rating.objects.create(value=f.random_int(min=-20, max=1000)).id
            q = Question.objects.create(
                author_id=choice(author_ids),
                title=f.sentence()[:128],
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                rating_id=r_id
            )
            for j in range(f.random_int(min=1, max=max_answers)):
                r_id = Rating.objects.create(value=f.random_int(min=-10, max=100)).id
                a = Answer.objects.create(
                    text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                    author_id=choice(author_ids),
                    rating_id=r_id,
                    question_id=q.id,
                    is_correct=f.random_element((True, False))
                )
            for i in range(f.random_int(min=1, max=2)):
                q.tags.add(choice(tags_ids))
