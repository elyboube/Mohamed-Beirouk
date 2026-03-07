from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Stay(models.Model):
    STAY_TYPES = [
        ("hotel", "Hotel"),
        ("guesthouse", "Guest House"),
        ("hostel", "Hostel"),
    ]

    name = models.CharField(max_length=200)
    stay_type = models.CharField(max_length=20, choices=STAY_TYPES, default="hotel")
    city = models.CharField(max_length=120)
    start_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="السعر باللأوقية (UM)")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    address = models.CharField(max_length=250, blank=True)
    latitude = models.FloatField(blank=True, null=True, help_text="خط العرض")
    longitude = models.FloatField(blank=True, null=True, help_text="خط الطول")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StayMedia(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="media")
    kind = models.CharField(max_length=20, choices=[("image", "Image"), ("video", "Video")], default="image")
    file = models.FileField(upload_to="stays/", blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.stay.name} - {self.kind}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("confirmed", "Confirmé"),
        ("cancelled", "Annulé"),
    ]
    
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="السعر الإجمالي باللأوقية (UM)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user} - {self.stay} ({self.check_in} to {self.check_out})"

    def clean(self):
        # ensure check_out after check_in
        if self.check_out and self.check_in and self.check_out <= self.check_in:
            from django.core.exceptions import ValidationError
            raise ValidationError("Check-out date must be after check-in date")

    def save(self, *args, **kwargs):
        # compute total_price first so validation can check non-null value
        if self.stay and self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            if nights < 0:
                nights = 0
            self.total_price = self.stay.start_price * nights * (self.guests or 1)
        # validate dates and fields before saving
        # full_clean will call clean() and raise ValidationError if needed
        self.full_clean()
        super().save(*args, **kwargs)

class StayFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_stays")
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'stay')
    
    def __str__(self):
        return f"{self.user} ♥ {self.stay}"