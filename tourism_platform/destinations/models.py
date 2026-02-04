from django.db import models

from django.db import models

class HomeVideo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="home_videos/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f"Home video #{self.id}"
    
class Destination(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=120)
    city = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Media(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="media")
    kind = models.CharField(max_length=20, choices=[("image", "Image"), ("video", "Video")], default="image")
    file = models.ImageField(upload_to="destinations/", blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.destination.name} - {self.kind}"