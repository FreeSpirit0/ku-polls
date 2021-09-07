import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    @admin.display(
        boolean=True,
        ordering='publication_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publication_date <= now

    def is_published(self):
        now = timezone.now()
        return now >= self.publication_date

    def can_vote(self):
        now = timezone.now()
        return self.publication_date <= now <= self.end_date

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
