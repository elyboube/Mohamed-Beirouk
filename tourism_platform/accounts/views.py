from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, ContactForm
from django.contrib.auth.decorators import login_required
from destinations.models import DestinationFavorite
from stays.models import StayFavorite, Booking, Stay

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.send_email():
                messages.success(request, "تم إرسال رسالتك بنجاح! سنرد عليك قريباً")
                return redirect("contact")
            else:
                messages.error(request, "حدث خطأ في إرسال الرسالة. يرجى المحاولة لاحقاً")
    else:
        form = ContactForm()

    return render(request, "accounts/contact.html", {"form": form})
@login_required
def dashboard(request):
    dest_favs = DestinationFavorite.objects.filter(user=request.user)
    stay_favs = StayFavorite.objects.filter(user=request.user)
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/dashboard.html", {
        "dest_favs": dest_favs,
        "stay_favs": stay_favs,
        "bookings": bookings,
    })


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "accounts/booking_detail.html", {"booking": booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        if booking.status == "pending":
            booking.status = "cancelled"
            booking.save()
            messages.success(request, "تم إلغاء الحجز بنجاح")
            return redirect("booking_detail", booking_id=booking.id)
        else:
            messages.error(request, "لا يمكن إلغاء حجز مؤكد أو ملغى بالفعل")
            return redirect("booking_detail", booking_id=booking.id)
    return render(request, "accounts/cancel_booking.html", {"booking": booking})
