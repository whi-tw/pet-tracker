from django.contrib import admin

from . import models as app_models

admin.site.register(app_models.Pet)
admin.site.register(app_models.HealthEvent)
admin.site.register(app_models.VetAppointment)
