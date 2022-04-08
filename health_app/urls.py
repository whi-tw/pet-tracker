from django.urls import path

from . import views

urlpatterns = [path("pet_image", views.pet_image, name="pet_image")]
