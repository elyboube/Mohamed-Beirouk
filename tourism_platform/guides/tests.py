from django.test import TestCase
from django.urls import reverse
from .models import Guide


class GuideViewsTest(TestCase):
    def setUp(self):
        self.g1 = Guide.objects.create(name="Ahmed", city="C1", price_per_day=100, languages="عربي, English")
        self.g2 = Guide.objects.create(name="Marie", city="C2", price_per_day=150, languages="French, عربي")
        self.g3 = Guide.objects.create(name="Hassan", city="C1", price_per_day=80, languages="عربي")

    def test_list(self):
        resp = self.client.get(reverse("guide_list"))
        self.assertContains(resp, "Ahmed")
        self.assertContains(resp, "Marie")
        self.assertContains(resp, "Hassan")

    def test_detail(self):
        resp = self.client.get(reverse("guide_detail", args=[self.g1.pk]))
        self.assertContains(resp, "Ahmed")

    def test_filter_by_city(self):
        url = reverse("guide_list")
        resp = self.client.get(url, {"city": "C1"})
        self.assertContains(resp, "Ahmed")
        self.assertContains(resp, "Hassan")
        self.assertNotContains(resp, "Marie")

    def test_filter_by_language(self):
        url = reverse("guide_list")
        resp = self.client.get(url, {"language": "French"})
        self.assertContains(resp, "Marie")
        self.assertNotContains(resp, "Ahmed")
        self.assertNotContains(resp, "Hassan")

    def test_filter_by_max_price(self):
        url = reverse("guide_list")
        resp = self.client.get(url, {"max_price": "100"})
        self.assertContains(resp, "Ahmed")
        self.assertContains(resp, "Hassan")
        self.assertNotContains(resp, "Marie")

    def test_filter_by_city_and_price(self):
        url = reverse("guide_list")
        resp = self.client.get(url, {"city": "C1", "max_price": "90"})
        self.assertContains(resp, "Hassan")
        self.assertNotContains(resp, "Ahmed")
        self.assertNotContains(resp, "Marie")

    def test_filter_by_language_and_city(self):
        url = reverse("guide_list")
        resp = self.client.get(url, {"language": "عربي", "city": "C2"})
        self.assertContains(resp, "Marie")
        self.assertNotContains(resp, "Ahmed")
        self.assertNotContains(resp, "Hassan")

    def test_clear_filters(self):
        url = reverse("guide_list")
        resp = self.client.get(url)
        self.assertEqual(resp.context['city'], '')
        self.assertEqual(resp.context['language'], '')
        self.assertEqual(resp.context['max_price'], '')

