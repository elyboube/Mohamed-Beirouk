from django.shortcuts import render, get_object_or_404
from .models import Stay

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

    context = {
        "items": qs,
        "city": city,
        "min_price": min_price,
        "max_price": max_price,
        "min_rating": min_rating,
    }
    return render(request, "stays/list.html", context)

def stay_detail(request, pk):
    item = get_object_or_404(Stay, pk=pk)

    images = item.media.filter(kind="image", file__isnull=False)

    return render(request, "stays/detail.html", {
        "item": item,
        "images": images,
    })