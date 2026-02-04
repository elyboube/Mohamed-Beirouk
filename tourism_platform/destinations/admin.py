from django.contrib import admin
from .models import Destination, Activity, Media
from .models import HomeVideo

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "is_published")
    list_filter = ("region", "is_published")
    search_fields = ("name", "region")

admin.site.register(Activity)
admin.site.register(Media)


@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order")
    list_editable = ("is_published", "order")
    ordering = ("order", "-id")