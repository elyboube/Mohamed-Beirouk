from django.urls import path
from . import views

urlpatterns = [
    path("", views.stay_list, name="stay_list"),
    path("<int:pk>/", views.stay_detail, name="stay_detail"),
]