from django.http import HttpRequest, FileResponse
from django.shortcuts import render

from .models import Pet


def pet_image(request: HttpRequest) -> FileResponse:
    pet_id = request.GET.get("id")
    pet = Pet.objects.get(id=pet_id)
    img = pet.picture.open("rb")
    img_ext = img.name.split(".")[-1]
    response_filename = f"{pet.name.lower()}.{img_ext}"
    response = FileResponse(img, filename=response_filename)
    return response
