import os
import random
from uuid import uuid4

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Pet(models.Model):
    name = models.CharField(max_length=200)

    def pet_photo_file_name(self, filename):
        ext = filename.split(".")[-1]
        filename = f"{str(uuid4())}.{ext}"
        return os.path.join("pet_photos", filename)

    def default_pet_photo():
        img_number = random.randint(0, 99)
        return os.path.join("default_pet_photos", f"{img_number}.jpg")

    picture = models.ImageField(
        blank=True, upload_to=pet_photo_file_name, default=default_pet_photo()
    )
    picture_profile = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    picture_icon = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 60},
    )

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def age(self) -> str:
        import arrow

        age = arrow.get(self.date_of_birth).humanize(
            only_distance=True, granularity=["year", "month"]
        )
        return age

    def __str__(self) -> str:
        return f"{self.name} - {self.species} {self.breed}`"


class PetEvent(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateTimeField("Date")


class VetAppointment(PetEvent):
    pass


class HealthEvent(PetEvent):
    pass
