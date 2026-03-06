from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from stays.models import Stay, Booking
from datetime import date, timedelta


class RegistrationTests(TestCase):
    def test_signup_page_loads(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "إنشاء حساب")

    def test_user_can_register(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "pass1234",
            "password2": "pass1234",
        }
        resp = self.client.post(reverse("signup"), data)
        self.assertEqual(resp.status_code, 302)
        u = User.objects.get(username="newuser")
        self.assertEqual(u.email, "new@example.com")


class ContactTests(TestCase):
    def test_contact_page_loads(self):
        resp = self.client.get(reverse("contact"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "تواصل معنا")


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dash", password="pwd")
    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 302)
    def test_dashboard_shows_empty(self):
        self.client.login(username="dash", password="pwd")
        resp = self.client.get(reverse("dashboard"))
        self.assertContains(resp, "لوحة التحكم")
        self.assertContains(resp, "لم تقم بأي حجوزات بعد")
    def test_dashboard_shows_bookings(self):
        self.client.login(username="dash", password="pwd")
        stay = Stay.objects.create(name="Test Hotel", city="Cairo", start_price=100)
        checkin = date.today()
        checkout = checkin + timedelta(days=2)
        booking = Booking.objects.create(user=self.user, stay=stay, check_in=checkin, check_out=checkout, guests=2)
        resp = self.client.get(reverse("dashboard"))
        self.assertContains(resp, "Test Hotel")
        self.assertContains(resp, "Cairo")


class BookingDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="book", password="pwd")
        self.other_user = User.objects.create_user(username="other", password="pwd")
        self.stay = Stay.objects.create(name="Test Hotel", city="Cairo", start_price=100)
        self.checkin = date.today()
        self.checkout = self.checkin + timedelta(days=2)
        self.booking = Booking.objects.create(user=self.user, stay=self.stay, check_in=self.checkin, check_out=self.checkout, guests=1)
    
    def test_booking_detail_requires_login(self):
        url = reverse("booking_detail", args=[self.booking.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
    
    def test_booking_detail_shows_info(self):
        self.client.login(username="book", password="pwd")
        url = reverse("booking_detail", args=[self.booking.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Hotel")
        self.assertContains(resp, "تفاصيل الحجز")
    
    def test_user_cannot_view_other_bookings(self):
        self.client.login(username="other", password="pwd")
        url = reverse("booking_detail", args=[self.booking.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
    
    def test_cancel_booking_requires_post(self):
        self.client.login(username="book", password="pwd")
        url = reverse("cancel_booking", args=[self.booking.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "تأكيد")
    
    def test_cancel_booking_pending(self):
        self.client.login(username="book", password="pwd")
        url = reverse("cancel_booking", args=[self.booking.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "cancelled")
    
    def test_cannot_cancel_confirmed(self):
        self.booking.status = "confirmed"
        self.booking.save()
        self.client.login(username="book", password="pwd")
        url = reverse("cancel_booking", args=[self.booking.id])
        resp = self.client.post(url)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")
