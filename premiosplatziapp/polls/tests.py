import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions that pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Pregunta del futuro?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_time_questions(self):
        """was_published_recently returns False for questions that pub_date is in the present time"""
        time = timezone.now() - datetime.timedelta(hours=23)
        future_question = Question(question_text="¿Pregunta del presente?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions that pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        future_question = Question(question_text="¿Pregunta del pasado?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """If no question existe, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_no_future_questions(self):
        """No future questions in the views until his pub_time is equal to the present time"""
        response = self.client.get(reverse("polls:index")) # Peticion http
        self.assertEqual(response.status_code, 200)
        time = timezone.now() + datetime.timedelta(days=5)
        future_question = Question(question_text="¿Pregunta futura?", pub_date=time)
        self.assertNotIn(future_question, response.context['latest_question_list'])