from django.contrib import admin
from .models import Stay, StayMedia, Booking, StayFavorite

class StayMediaInline(admin.TabularInline):
    model = StayMedia
    extra = 1

@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "start_price", "rating", "stay_type")
    list_filter = ("stay_type", "city")
    search_fields = ("name", "city")
    inlines = [StayMediaInline]
    fieldsets = (
        ("Informations", {
            "fields": ("name", "stay_type", "city", "address")
        }),
        ("Prix & Évaluation", {
            "fields": ("start_price", "rating")
        }),
        ("Description", {
            "fields": ("description",)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "stay", "check_in", "check_out", "status", "total_price")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "stay__name")
    readonly_fields = ("created_at", "total_price")

@admin.register(StayFavorite)
class StayFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "stay", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username", "stay__name")