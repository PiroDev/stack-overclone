from django.db import models
from .managers import *

class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    tags = models.ManyToManyField('questions.Tag', verbose_name='Tags')
    author = models.ForeignKey('users.UserProfile', verbose_name='Author', on_delete=models.CASCADE)
    rating = models.OneToOneField('questions.Rating', verbose_name='Rating', on_delete=models.CASCADE)

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def get_answers(self):
        query_set = self.answer_set.order_by('-rating__value', '-date_created').all()
        return query_set

    def get_count_answers(self):
        return self.get_answers().count()

    def get_tags(self):
        query_set = self.tags.all()
        return query_set

    def __str__(self):
        return self.author.__str__() + ': ' + self.title

class Answer(models.Model):
    text = models.TextField(verbose_name='Text')
    is_correct = models.BooleanField(default=False, verbose_name='Correct')
    date_created = models.DateField(auto_now_add=True, verbose_name='Date created')
    author = models.ForeignKey('users.UserProfile', verbose_name='Author', on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', verbose_name='Question', on_delete=models.CASCADE)
    rating = models.OneToOneField('questions.Rating', verbose_name='Rating', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.author.__str__()

class Tag(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='Title')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Rating(models.Model):
    value = models.IntegerField(default=0, verbose_name='Value')
    users_up_voted = models.ManyToManyField('users.UserProfile', blank=True, related_name='users_up_voted')
    users_down_voted = models.ManyToManyField('users.UserProfile', blank=True, related_name='users_down_voted')

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return str(self.value)

    def has_user_up_voted(self, user):
        return self.users_up_voted.filter(user=user).count() == 0

    def has_user_down_voted(self, user):
        return self.users_down_voted.filter(user=user).count() == 0

    def up_vote(self, user):
        if self.has_user_up_voted(user):
            self.users_up_voted.remove(user)
            self.value -= 1
        elif self.has_user_down_voted(user):
            self.users_down_voted.remove(user)
            self.users_up_voted.add(user)
            self.value += 2
        else:
            self.users_up_voted.add(user)
            self.value += 1

    def down_vote(self, user):
        if self.has_user_down_voted(user):
            self.users_down_voted.remove(user)
            self.value += 1
        elif self.has_user_up_voted(user):
            self.users_up_voted.remove(user)
            self.users_down_voted.add(user)
            self.value -= 2
        else:
            self.users_down_voted.add(user)
            self.value -= 1


