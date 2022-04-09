from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.template import loader, TemplateDoesNotExist, Template
from django.urls import reverse

import sweetify


from .models import Pet
from .forms import PetUpdateForm


def template_context(segment: str, request: HttpRequest, **kwargs):
    context = {"segment": segment}
    if request.user:
        context["user_pets"] = list(Pet.objects.filter(owner=request.user))
    context.update(kwargs)
    return context


@login_required(login_url="/login/")
def pet_overview(request: HttpRequest, pet_id: int) -> HttpResponse:
    this_pet: Pet = get_object_or_404(Pet, id=pet_id)
    form = PetUpdateForm(request.POST or None, instance=this_pet)
    context = template_context(
        "/".join(request.path.split("/")[-2:]),
        request,
        pet=this_pet,
        form=form,
    )
    if form.is_valid():
        this_pet = form.save(commit=False)
        this_pet.save()
        sweetify.toast(
            request,
            f"{this_pet.name} was updated successfully.",
            "success",
            position="top-end",
        )
    return render(request, "pets/pet_overview.html", context)


@login_required(login_url="/login/")
def index(request: HttpRequest) -> HttpResponse:
    context = template_context("index", request)

    html_template = loader.get_template("pets/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request: HttpRequest) -> HttpResponse:
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context = template_context(load_template, request)
        print(context)

        html_template = loader.get_template("pets/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except TemplateDoesNotExist:
        html_template = loader.get_template("pets/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("pets/page-500.html")
        return HttpResponse(html_template.render(context, request))
