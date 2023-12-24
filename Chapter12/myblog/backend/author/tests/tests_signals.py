from django.test import TestCase
from django.db.models import signals

from author.models import Author
from author.receivers import my_handler


class SignalsTest(TestCase):
    def test_connection(self):
        result = signals.post_save.disconnect(
           receiver=my_handler, sender=Author
        )
        self.assertTrue(result)
