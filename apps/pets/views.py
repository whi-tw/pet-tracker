from typing import Union
from django import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse

import sweetify


from .models import Pet, PetEvent, VetAppointment, HealthEvent
from .forms import PetUpdateForm, VetAppointmentUpdateForm, HealthEventUpdateForm


def template_context(segment: str, request: HttpRequest, **kwargs):
    context = {"segment": segment}
    if request.user:
        context["user_pets"] = list(Pet.objects.filter(owner=request.user))
    context.update(kwargs)
    return context


@login_required(login_url="/login/")
def pet_overview(request: HttpRequest, pet_id: int) -> HttpResponse:
    this_pet: Pet = get_object_or_404(Pet, id=pet_id)
    vet_appointments = VetAppointment.objects.filter(pet=this_pet)
    health_events = HealthEvent.objects.filter(pet=this_pet)
    timeline_entries = {}
    for event in PetEvent.objects.filter(pet=this_pet).order_by("-date"):
        event_date = event.date.date()
        if event_date not in timeline_entries.keys():
            timeline_entries[event_date] = []
        timeline_entries[event_date].append(event)
    form = PetUpdateForm(request.POST or None, instance=this_pet)
    context = template_context(
        "/".join(request.path.split("/")[-2:]),
        request,
        pet=this_pet,
        vet_appointments=vet_appointments,
        health_events=health_events,
        timeline_entries=timeline_entries,
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


@login_required(login_url="/login/")
def event_edit(request: HttpRequest, kind: str, id: int) -> HttpResponse:
    model: PetEvent
    form: forms.Form
    match kind:
        case "vetappointment":
            model = VetAppointment
            form = VetAppointmentUpdateForm
        case "healthevent":
            model = HealthEvent
            form = HealthEventUpdateForm
        case _:
            return HttpResponseBadRequest(f"Kind {kind} is not valid.")
    obj = get_object_or_404(model, id=id)
    form = form(request.POST or None, instance=obj)
    event: PetEvent = get_object_or_404(model, id=id)
    context = {"event": event, "form": form}
    html_template = loader.get_template("pets/modal-form.html")
    return HttpResponse(html_template.render(context, request))
