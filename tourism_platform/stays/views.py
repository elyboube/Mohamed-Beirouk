from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Stay, StayFavorite, Booking
from .forms import BookingForm

def stay_list(request):
    qs = Stay.objects.all().order_by("name")

    city = request.GET.get("city", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    min_rating = request.GET.get("min_rating", "").strip()

    if city:
        qs = qs.filter(city__icontains=city)
    if min_price:
        qs = qs.filter(start_price__gte=min_price)
    if max_price:
        qs = qs.filter(start_price__lte=max_price)
    if min_rating:
        qs = qs.filter(rating__gte=min_rating)

    cities = Stay.objects.values_list('city', flat=True).distinct()

    # Handle comparison selection
    compare_ids = request.GET.getlist('compare') or request.GET.get('ids', '').split(',') if request.GET.get('ids') else []
    compare_stays = []
    if compare_ids:
        try:
            compare_ids = [int(id.strip()) for id in compare_ids if id.strip()]
            compare_stays = Stay.objects.filter(id__in=compare_ids)
        except (ValueError, TypeError):
            compare_ids = []
            compare_stays = []

    context = {
        "items": qs,
        "cities": cities,
        "city": city,
        "min_price": min_price,
        "max_price": max_price,
        "min_rating": min_rating,
        "compare_stays": compare_stays,
        "compare_ids": compare_ids,
    }
    return render(request, "stays/list.html", context)

def stay_comparison(request):
    ids_string = request.GET.get('ids', '')
    if not ids_string:
        return redirect('stay_list')
    
    try:
        compare_ids = [int(id.strip()) for id in ids_string.split(',') if id.strip()]
    except ValueError:
        return redirect('stay_list')
    
    stays = Stay.objects.filter(id__in=compare_ids)
    if not stays:
        return redirect('stay_list')
    
    return render(request, "stays/comparison.html", {
        "stays": stays,
    })

def stay_detail(request, pk):
    item = get_object_or_404(Stay, pk=pk)
    images = item.media.filter(kind="image", file__isnull=False)
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = StayFavorite.objects.filter(user=request.user, stay=item).exists()

    # booking form
    booking_form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                bk = booking_form.save(commit=False)
                bk.stay = item
                bk.user = request.user
                bk.save()
                return redirect("stay_detail", pk=item.id)
        else:
            booking_form = BookingForm()

    return render(request, "stays/detail.html", {
        "item": item,
        "images": images,
        "is_favorite": is_favorite,
        "booking_form": booking_form,
    })

@login_required
def add_favorite(request, content_type, pk):
    """Add to favorites: destination or stay"""
    if content_type == "destination":
        from destinations.models import Destination, DestinationFavorite
        destination = get_object_or_404(Destination, pk=pk)
        DestinationFavorite.objects.get_or_create(user=request.user, destination=destination)
        return JsonResponse({"status": "added"})
    elif content_type == "stay":
        stay = get_object_or_404(Stay, pk=pk)
        StayFavorite.objects.get_or_create(user=request.user, stay=stay)
        return JsonResponse({"status": "added"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def remove_favorite(request, content_type, pk):
    """Remove from favorites"""
    if content_type == "destination":
        from destinations.models import Destination, DestinationFavorite
        destination = get_object_or_404(Destination, pk=pk)
        DestinationFavorite.objects.filter(user=request.user, destination=destination).delete()
        return JsonResponse({"status": "removed"})
    elif content_type == "stay":
        stay = get_object_or_404(Stay, pk=pk)
        StayFavorite.objects.filter(user=request.user, stay=stay).delete()
        return JsonResponse({"status": "removed"})
    return JsonResponse({"status": "error"}, status=400)