from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Stay, Booking
from datetime import date, timedelta


class StayViewsTest(TestCase):
    def setUp(self):
        self.stay = Stay.objects.create(name="HotelX", city="CityY", start_price=50)
        self.user = User.objects.create_user(username="tester", password="pwd")

    def test_list_and_filter(self):
        url = reverse("stay_list")
        resp = self.client.get(url)
        self.assertContains(resp, "HotelX")
        # filter by city
        resp = self.client.get(url, {"city": "CityY"})
        self.assertContains(resp, "HotelX")

    def test_detail_and_favorite(self):
        url = reverse("stay_detail", args=[self.stay.pk])
        resp = self.client.get(url)
        self.assertContains(resp, "HotelX")
        # check favorite flag for anonymous
        self.assertFalse(resp.context.get("is_favorite"))

        # login and add favorite via endpoint
        self.client.login(username="tester", password="pwd")
        add_url = reverse("add_favorite", args=["stay", self.stay.pk])
        resp = self.client.post(add_url)
        self.assertEqual(resp.json().get("status"), "added")
        resp = self.client.get(url)
        self.assertTrue(resp.context.get("is_favorite"))
        # remove
        remove_url = reverse("remove_favorite", args=["stay", self.stay.pk])
        resp = self.client.post(remove_url)
        self.assertEqual(resp.json().get("status"), "removed")
        resp = self.client.get(url)
        self.assertFalse(resp.context.get("is_favorite"))

    def test_booking(self):
        self.client.login(username="tester", password="pwd")
        checkin = date.today()
        checkout = checkin + timedelta(days=1)
        booking = Booking.objects.create(user=self.user, stay=self.stay, check_in=checkin, check_out=checkout, guests=2)
        self.assertEqual(self.user.booking_set.count(), 1)
        # price should be calculated automatically
        self.assertEqual(booking.total_price, self.stay.start_price * 1 * 2)

    def test_booking_via_view(self):
        self.client.login(username="tester", password="pwd")
        url = reverse("stay_detail", args=[self.stay.pk])
        checkin = date.today()
        checkout = checkin + timedelta(days=2)
        resp = self.client.post(url, {"check_in": checkin, "check_out": checkout, "guests": 3})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Booking.objects.filter(user=self.user, stay=self.stay).exists())
        booking = Booking.objects.get(user=self.user, stay=self.stay)
        expected = self.stay.start_price * 2 * 3
        self.assertEqual(booking.total_price, expected)

    def test_booking_total_price_calculation(self):
        self.client.login(username="tester", password="pwd")
        checkin = date.today()
        checkout = checkin + timedelta(days=3)
        booking = Booking.objects.create(user=self.user, stay=self.stay, check_in=checkin, check_out=checkout, guests=2)
        expected = self.stay.start_price * 3 * 2
        self.assertEqual(booking.total_price, expected)

    def test_invalid_dates_raise(self):
        # check_out before or equal to check_in should raise ValidationError on save
        self.client.login(username="tester", password="pwd")
        with self.assertRaises(Exception):
            Booking.objects.create(user=self.user, stay=self.stay, check_in=date.today(), check_out=date.today() - timedelta(days=1), guests=1)

