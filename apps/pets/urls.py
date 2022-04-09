from django.urls import path, re_path

from . import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("pets/<int:pet_id>", views.pet_overview, name="pet_overview"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
