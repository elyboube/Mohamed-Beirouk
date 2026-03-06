from django.test import TestCase
from django.urls import reverse
from .models import Guide


class GuideViewsTest(TestCase):
    def setUp(self):
        self.g = Guide.objects.create(name="Ahmed", city="C1", price_per_day=100)

    def test_list(self):
        resp = self.client.get(reverse("guide_list"))
        self.assertContains(resp, "Ahmed")

    def test_detail(self):
        resp = self.client.get(reverse("guide_detail", args=[self.g.pk]))
        self.assertContains(resp, "Ahmed")

