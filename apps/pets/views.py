import os
import random
from typing import Union

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    FileResponse,
    HttpResponseNotFound,
    HttpResponse,
    HttpResponseRedirect,
)
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse

from core import settings

from .models import Pet


@login_required(login_url="/login/")
def pet_image(request: HttpRequest) -> Union[FileResponse, HttpResponseNotFound]:
    try:
        pet_id = request.GET.get("id")
        pet: Pet = Pet.objects.get(id=pet_id)
        img = pet.picture.open("rb")
        img_ext = img.name.split(".")[-1]
        response_filename = f"{pet.name.lower()}.{img_ext}"
        response = FileResponse(img, filename=response_filename)
    except ObjectDoesNotExist:
        response = HttpResponseNotFound()
    except ValueError:
        rng = random.Random(pet.name)
        img_number = rng.randint(0, 99)
        img_path = os.path.join(
            settings.MEDIA_ROOT, "default_pet_photos", f"{img_number}.jpg"
        )
        print(img_path)
        img = open(img_path, "rb")
        response = FileResponse(img, filename="default.jpeg")

    return response


@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}

    html_template = loader.get_template("pets/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("pets/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except TemplateDoesNotExist:

        html_template = loader.get_template("pets/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("pets/page-500.html")
        return HttpResponse(html_template.render(context, request))
