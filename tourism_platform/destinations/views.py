from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from .models import Destination, HomeVideo, DestinationReview, DestinationFavorite
from .forms import DestinationReviewForm
from guides.models import Guide
from stays.models import Stay


def destination_detail(request, pk):
    item = get_object_or_404(Destination, pk=pk, is_published=True)
    place = item.name.strip()
    region = item.region.strip()

    # Guides
    guides_qs = Guide.objects.filter(
        city__icontains=place
    ).order_by("price_per_day")

    if not guides_qs.exists():
        guides_qs = Guide.objects.filter(
            city__icontains=region
        ).order_by("price_per_day")

    related_guides = guides_qs[:3]

    # Stays
    stays_qs = Stay.objects.filter(
        city__icontains=place
    ).order_by("start_price")

    if not stays_qs.exists():
        stays_qs = Stay.objects.filter(
            city__icontains=region
        ).order_by("start_price")

    related_stays = stays_qs[:3]

    # Images
    images = item.media.filter(kind="image").exclude(file="")
    
    # Reviews
    reviews = item.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # review form
    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DestinationReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.destination = item
                review.user = request.user
                review.save()
                return redirect("destination_detail", pk=item.id)
        else:
            form = DestinationReviewForm()

    # User favorite status
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = DestinationFavorite.objects.filter(user=request.user, destination=item).exists()

    return render(request, "destinations/detail.html", {
        "item": item,
        "images": images,
        "related_guides": related_guides,
        "related_stays": related_stays,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "is_favorite": is_favorite,
        "form": form,
    })

def destination_list(request):
    items = Destination.objects.filter(is_published=True)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        items = items.filter(
            Q(name__icontains=search) | 
            Q(region__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Filter by region
    region = request.GET.get('region', '')
    if region:
        items = items.filter(region__icontains=region)
    
    # Sort
    sort = request.GET.get('sort', '-id')
    items = items.order_by(sort)
    
    # Regions for filter dropdown
    regions = Destination.objects.filter(is_published=True).values_list('region', flat=True).distinct()
    
    return render(request, "destinations/list.html", {
        "items": items,
        "regions": regions,
        "search": search,
        "selected_region": region,
    })


def home(request):
    featured_destinations = Destination.objects.filter(is_published=True).order_by("-id")[:3]
    featured_guides = Guide.objects.order_by("-id")[:3]
    cheapest_stays = Stay.objects.order_by("start_price")[:3]

    home_videos = HomeVideo.objects.filter(is_published=True).order_by("-id")[:6]

    return render(request, "home.html", {
        "featured_destinations": featured_destinations,
        "featured_guides": featured_guides,
        "cheapest_stays": cheapest_stays,
        "home_videos": home_videos,
    })