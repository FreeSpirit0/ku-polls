"""All models for the polls app."""
import datetime
from django.contrib import admin
from django.contrib.auth.models import User
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

    @property
    def votes(self) -> int:
        """Return votes amount of that choice.
        Returns:
            int: votes amount
        """
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return the choice text as the representation of this model."""
        return self.choice_text


class Vote(models.Model):
    """Model for votes of question"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self) -> Question:
        """Return the question holding this vote.
        Returns:
            Question: question of this vote.
        """
        return self.choice.question

