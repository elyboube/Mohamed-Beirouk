from django.contrib import admin
from .models import Destination, Activity, Media, DestinationReview, DestinationFavorite
from .models import HomeVideo

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "rating", "is_published")
    list_filter = ("region", "is_published")
    search_fields = ("name", "region", "city")
    fieldsets = (
        ("Informations de base", {
            "fields": ("name", "region", "city", "description")
        }),
        ("Coordonnées", {
            "fields": ("latitude", "longitude")
        }),
        ("Détails", {
            "fields": ("best_time_to_visit", "rating", "is_published")
        }),
    )

admin.site.register(Activity)
admin.site.register(Media)

@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ("destination", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("destination__name", "user__username")
    readonly_fields = ("created_at",)

@admin.register(DestinationFavorite)
class DestinationFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "destination", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username", "destination__name")

@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order")
    list_editable = ("is_published", "order")
    ordering = ("order", "-id")