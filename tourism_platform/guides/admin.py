from django.contrib import admin
from .models import Guide, GuideReview, GuideMedia

class GuideMediaInline(admin.TabularInline):
    model = GuideMedia
    extra = 1

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "price_per_day")
    inlines = [GuideMediaInline]

@admin.register(GuideReview)
class GuideReviewAdmin(admin.ModelAdmin):
    list_display = ("guide", "user", "rating", "created_at")