from django.db import models

class QuestionManager(models.Manager):
    def get_new(self):
        query_set = super().order_by('-date_created').all()
        return query_set

    def get_top_rated(self):
        query_set = super().order_by('-rating__value').all()
        return query_set

    def get_by_tag(self, tag_title):
        query_set = super().filter(tags__title=tag_title).all()
        return query_set

