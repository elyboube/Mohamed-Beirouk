from django.db import models
from django.conf import settings

class Guide(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=120)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    languages = models.CharField(max_length=200, help_text="مثال: عربي, English, Français")
    specialties = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class GuideMedia(models.Model):
    guide = models.ForeignKey(Guide, related_name="media", on_delete=models.CASCADE)

    kind = models.CharField(
        max_length=20,
        choices=[("image", "Image"), ("video", "Video")],
        default="image"
    )

    file = models.FileField(upload_to="guides/", blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.guide.name} - {self.kind}"
class GuideReview(models.Model):
    guide = models.ForeignKey("Guide", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="guide_reviews", )
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    