import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Attribute
from django.urls import reverse
class AttributeDetailViewTests(TestCase):
    def test_future_attribute(self):
        """
        The detail view of a attribute with a pub_date in the future
        returns a 404 not found.
        """
        future_attribute = create_attribute(attribute_text='Future attribute.', days=5)
        url = reverse('polls:detail', args=(future_attribute.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_attribute(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_attribute = create_attribute(attribute_text='Past Attribute.', days=-5)
        url = reverse('polls:detail', args=(past_attribute.id,))
        response = self.client.get(url)
        self.assertContains(response, past_attribute.attribute_text)

class AttributeModelTests(TestCase):
def create_attribute(attribute_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Attribute.objects.create(attribute_text=attribute_text, pub_date=time)


class AttributeIndexViewTests(TestCase):
    def test_no_attributes(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_attribute_list'], [])

    def test_past_attribute(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_attribute(attribute_text="Past attribute.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_attribute_list'],
            ['<Attribute: Past attribute.>']
        )

    def test_future_attribute(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_attribute(attribute_text="Future attribute.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_attribute_list'], [])

    def test_future_attribute_and_past_attribute(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_attribute(attribute_text="Past attribute.", days=-30)
        create_attribute(attribute_text="Future attribute.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_attribute_list'],
            ['<Attribute: Past attribute.>']
        )

    def test_two_past_attribute(self):
        """
        The questions index page may display multiple questions.
        """
        create_attribute(attribute_text="Past attribute 1.", days=-30)
        create_attribute(attribute_text="Past attribute 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_attribute_list'],
            ['<Attribute: Past attribute 2.>', '<Attribute: Past attribute 1.>']
        )

    def test_was_published_recently_with_future_attribute(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_attribute = Attribute(pub_date=time)
        self.assertIs(future_attribute.was_published_recently(), False)
        def test_was_published_recently_with_old_attribute(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_attribute = Attribute(pub_date=time)
    self.assertIs(old_attribute.was_published_recently(), False)

def test_was_published_recently_with_recent_attribute(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_attribute = Attribute(pub_date=time)
    self.assertIs(recent_attribute.was_published_recently(), True)
