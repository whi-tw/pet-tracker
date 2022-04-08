import os
from uuid import uuid4

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class VetVisit(models.Model):
    pass


class MedicalEvent(models.Model):
    pass


class Animal(models.Model):
    class SpeciesChoices(models.IntegerChoices):
        CAT = 1, _("Cat")
        DOG = 2, _("Dog")

    species = models.IntegerField(choices=SpeciesChoices.choices)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField("Date of Birth", default=datetime.fromtimestamp(0))

    class SexChoices(models.IntegerChoices):
        FEMALE = 1, _("Female")
        MALE = 2, _("Male")
        UNKNOWN = 3, _("Unknown")

    sex = models.IntegerField(
        choices=SexChoices.choices,
        default=SexChoices.UNKNOWN,
    )

    def __str__(self) -> str:
        return f"{self.get_species_display()} ({self.breed})"


class Pet(models.Model):
    name = models.CharField(max_length=200)

    animal = models.OneToOneField(
        Animal, verbose_name=_("Animal Details"), on_delete=models.CASCADE
    )

    def pet_photo_file_name(self, filename):
        ext = filename.split(".")[-1]
        filename = f"{str(uuid4())}.{ext}"
        return os.path.join("pet_photos", str(self.id), filename)

    picture = models.ImageField(blank=True, upload_to=pet_photo_file_name)

    vet_visits = models.ForeignKey(VetVisit, on_delete=models.CASCADE, null=True)
    medical_event = models.ForeignKey(MedicalEvent, on_delete=models.CASCADE, null=True)

    @property
    def age(self) -> str:
        import arrow

        dob: datetime = self.animal.date_of_birth
        age = arrow.get(dob).humanize(only_distance=True, granularity=["year", "month"])
        return age

    def __str__(self) -> str:
        return f"{self.name} - {self.animal}"
