from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Destination, DestinationReview


class DestinationViewsTest(TestCase):
    def setUp(self):
        self.dest = Destination.objects.create(name="Cairo", region="Egypt")
        self.user = User.objects.create_user(username="foo", password="bar")

    def test_list_and_search(self):
        url = reverse("destination_list")
        resp = self.client.get(url)
        self.assertContains(resp, "Cairo")

        # search by region
        resp = self.client.get(url, {"search": "Egypt"})
        self.assertContains(resp, "Cairo")

    def test_detail_and_review(self):
        url = reverse("destination_detail", args=[self.dest.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Cairo")

        # login and post review via view form
        self.client.login(username="foo", password="bar")
        resp = self.client.post(url, {"rating": 4, "comment": "Nice place"})
        # after POST should redirect back
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(DestinationReview.objects.filter(destination=self.dest, user=self.user, rating=4).exists())
        resp = self.client.get(url)
        self.assertContains(resp, "4")
        self.assertContains(resp, "Nice place")
        self.assertEqual(resp.context["avg_rating"], 4.0)

