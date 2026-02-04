from django.shortcuts import render, get_object_or_404, redirect
from .models import Guide
from .forms import GuideReviewForm

from destinations.models import Destination, HomeVideo
from stays.models import Stay

def home(request):
    featured_destinations = Destination.objects.filter(is_published=True).order_by("-id")[:3]
    featured_guides = Guide.objects.order_by("-id")[:3]
    cheapest_stays = Stay.objects.order_by("start_price")[:3]

    home_videos = HomeVideo.objects.filter(is_published=True).exclude(file="").order_by("order", "-id")[:6]

    return render(request, "home.html", {
        "featured_destinations": featured_destinations,
        "featured_guides": featured_guides,
        "cheapest_stays": cheapest_stays,
        "home_videos": home_videos,
    })

def guide_detail(request, pk):
    item = get_object_or_404(Guide, pk=pk)

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = GuideReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.guide = item
                review.user = request.user
                review.save()
                return redirect("guide_detail", pk=item.id)
        else:
            form = GuideReviewForm()

    reviews = item.reviews.all().order_by("-created_at")[:30]
    return render(request, "guides/detail.html", {"item": item, "reviews": reviews, "form": form})
def guide_list(request):
    qs = Guide.objects.all().order_by("name")

    city = request.GET.get("city", "").strip()
    language = request.GET.get("language", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if city:
        qs = qs.filter(city__icontains=city)
    if language:
        qs = qs.filter(languages__icontains=language)
    if max_price:
        qs = qs.filter(price_per_day__lte=max_price)

    context = {
        "items": qs,
        "city": city,
        "language": language,
        "max_price": max_price,
    }
    return render(request, "guides/list.html", context)