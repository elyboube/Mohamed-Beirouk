from django.db import models

class Stay(models.Model):
    STAY_TYPES = [
        ("hotel", "Hotel"),
        ("guesthouse", "Guest House"),
        ("hostel", "Hostel"),
    ]

    name = models.CharField(max_length=200)
    stay_type = models.CharField(max_length=20, choices=STAY_TYPES, default="hotel")
    city = models.CharField(max_length=120)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    address = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class StayMedia(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="media")
    kind = models.CharField(max_length=20, choices=[("image", "Image"), ("video", "Video")], default="image")
    file = models.FileField(upload_to="stays/", blank=True, null=True)  # يدعم صورة/فيديو
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.stay.name} - {self.kind}"