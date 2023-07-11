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


def create_question(question_text, days):
    """Create a question with the given question text
        and published the given number of days offset to now.
        (negative for questions published in the past, positive for question that have yet to be published)
    Args:
        question_text (_str_)
        days (_int_)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)


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
        future_question = create_question("¿Pregunta futura?", days=5)
        self.assertContains(response, "No polls are available.")
        self.assertNotIn(future_question, response.context['latest_question_list'])

    def test_past_questions(self):
        """Questions with a pub:date un the past are displayed on the index page"""
        past_question = create_question("¿Pregunta pasada?", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_future_question_and_past_question(self):
        """Even if both past and future questoin exist, just the past question are displayed """
        past_question = create_question("¿Past Question?", days=-30)
        future_question = create_question("¿Future Question?", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""   
        past_question_1 = create_question("¿Past Question 1?", days=-30)
        past_question_2 = create_question("¿Past Question 2?", days=-35)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question_1, past_question_2]
        )

    def test_two_future_questions(self):
        """The questions index page may no display multiple questions"""   
        future_question_1 = create_question("¿Future Question 1?", days=30)
        future_question_2 = create_question("¿Future Question 2?", days=35)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )


class QuestionDetailViewTest(TestCase):
    def test_future_questions(self):
        """The detail view of a question with a pub date in the future
            returns a 404 error not found.
        """ 
        future_question = create_question("¿Future Question?", days=30)
        url = reverse('polls:detail', args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub date in the past
            displays the question's text
        """
        past_question = create_question("¿Past Question?", days=-30)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ResultsViewTest(TestCase):
    def test_results_view(self):
        question = create_question("¿Cual es el mejor profesor?", days=0)

        # Simulacion de una votación
        choice = question.choice_set.create(choice_text="Martoni")
        choice.votes = 5
        choice.save()

        url = reverse('polls:results', args=(question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Respuesta tenga un estado HTTP 200 (OK)
        self.assertContains(response, question.question_text) # La pregunta se muestre correctamente en la respuesta
        self.assertContains(response, reverse('polls:detail', args=(question.id,))) # Verificar que el enlace para votar nuevamente se muestre correctamente en la respuesta