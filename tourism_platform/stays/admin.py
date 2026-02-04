from django.contrib import admin
from .models import Stay, StayMedia

class StayMediaInline(admin.TabularInline):
    model = StayMedia
    extra = 1

@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "start_price", "rating")
    inlines = [StayMediaInline]