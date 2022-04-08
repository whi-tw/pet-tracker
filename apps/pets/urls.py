from django.urls import path, re_path

from . import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
    path("pet_image", views.pet_image, name="pet_image"),
]
