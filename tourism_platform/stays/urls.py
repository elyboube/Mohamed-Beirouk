from django.urls import path
from . import views

urlpatterns = [
    path("", views.stay_list, name="stay_list"),
    path("comparison/", views.stay_comparison, name="stay_comparison"),
    path("<int:pk>/", views.stay_detail, name="stay_detail"),
    path("favorite/add/<str:content_type>/<int:pk>/", views.add_favorite, name="add_favorite"),
    path("favorite/remove/<str:content_type>/<int:pk>/", views.remove_favorite, name="remove_favorite"),
]