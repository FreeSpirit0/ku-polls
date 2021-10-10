"""All models for the polls app."""
import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Model for all questions."""

    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    @admin.display(
        boolean=True,
        ordering='publication_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return boolean whether it was published recently or not."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publication_date <= now

    def is_published(self):
        """Return boolean whether it was published or not."""
        now = timezone.now()
        return now >= self.publication_date

    def can_vote(self):
        """Return boolean whether the question are votable or not."""
        now = timezone.now()
        return self.publication_date <= now <= self.end_date

    def __str__(self):
        """Return the question text as the representation of this model."""
        return self.question_text


class Choice(models.Model):
    """Model for choices of question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the choice text as the representation of this model."""
        return self.choice_text
