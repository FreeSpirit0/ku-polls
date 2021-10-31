"""Module for testing models."""
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question


class QuestionModelTests(TestCase):
    """Test for question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose publication_date  is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose publication_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose publication_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False for questions whose publication_date is not arrived yet."""
        future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=future)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_past_question(self):
        """is_published() return True for questions whose publication_date are already passed."""
        past = timezone.now() - timezone.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=past)
        self.assertTrue(recent_question.is_published())

    def test_can_vote_with_votable_question(self):
        """can_vote() return True for questions whose current time are within the publication date and end date."""
        past = timezone.now() - timezone.timedelta(hours=23, minutes=59, seconds=59)
        future = timezone.now() + timezone.timedelta(hours=23, minutes=59, seconds=59)
        votable_question = Question(publication_date=past, end_date=future)
        self.assertTrue(votable_question.can_vote())

    def test_can_vote_with_unvotable_question(self):
        """can_vote() return False for questions whose current time aren't within the publication date and end date."""
        future = timezone.now() + timezone.timedelta(hours=23, minutes=59, seconds=59)
        unvotable_question = Question(publication_date=future)
        self.assertFalse(unvotable_question.can_vote())