from django.shortcuts import render, get_object_or_404
from .models import Destination, HomeVideo
from guides.models import Guide
from stays.models import Stay


def destination_detail(request, pk):
    # 1️⃣ جلب الوجهة
    item = get_object_or_404(Destination, pk=pk, is_published=True)

    # 2️⃣ تحديد مكان الربط
    place = item.name.strip()     # مثال: تجكجة
    region = item.region.strip()  # مثال: ولاية تكانت

    # 3️⃣ المرشدون
    guides_qs = Guide.objects.filter(
        city__icontains=place
    ).order_by("price_per_day")

    if not guides_qs.exists():
        guides_qs = Guide.objects.filter(
            city__icontains=region
        ).order_by("price_per_day")

    related_guides = guides_qs[:3]

    # 4️⃣ الإقامات
    stays_qs = Stay.objects.filter(
        city__icontains=place
    ).order_by("start_price")

    if not stays_qs.exists():
        stays_qs = Stay.objects.filter(
            city__icontains=region
        ).order_by("start_price")

    related_stays = stays_qs[:3]

    # 5️⃣ صور الوجهة (للسلايدر)
    images = item.media.filter(kind="image").exclude(file="")

    # 6️⃣ الإرسال إلى القالب
    return render(request, "destinations/detail.html", {
        "item": item,
        "images": images,
        "related_guides": related_guides,
        "related_stays": related_stays,
    })
def destination_list(request):
    items = Destination.objects.filter(is_published=True)
    return render(request, "destinations/list.html", {
        "items": items
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